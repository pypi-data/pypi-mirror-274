from pyspark.sql import SparkSession
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from datetime import datetime

from FabricFramework.FabricLocations import *
from FabricFramework.FabricDataInterface import *
from FabricFramework.DataSource import *
from FabricFramework.LogMonitor import *


class FabricConfiguration:
    """
    Configuration class for managing fabric data ingestion and validation processes.
    """

    def __init__(self, ingestConfiguration, constants, function=None, listofSourceSystems=None, listofSourceID=None):
        """
        Initialize the FabricConfiguration.

        Args:
            ingestConfiguration: Configuration for ingestion.
            constants: Dictionary containing constant values.
            function: Optional function to be applied during ingestion.
            listofSourceSystems: Optional list of source systems to filter by.
            listofSourceID: Optional list of source IDs to filter by.
        """
        self.spark = SparkSession.builder.appName("Default_Config").getOrCreate()
        self.fabricInterface = FabricDataInterface()
        self.ingestConfiguration = ingestConfiguration
        self.function = function
        self.constants = constants
        self.sources = self._filterSources(listofSourceSystems, listofSourceID)
        self.logger = Logger.getInstance(
            constants['LOGS_AZURE_TENANT_ID'], constants['LOGS_AZURE_CLIENT_ID'],
            constants['LOGS_AZURE_CLIENT_SECRET'], constants['DCE_ENDPOINT'],
            constants['DRC_ID'], constants['LOG_BUFFER_SIZE']
        )
        self.entity_log_stream = constants['LOG_STREAM']

    def flushLogs(self):
        """
        Flush the logs to the log stream.
        """
        self.logger.flushLogs(self.entity_log_stream)

    def _filterSources(self, listofSourceSystems=None, listofSourceID=None):
        """
        Filter the sources based on the provided source systems and source IDs.

        Args:
            listofSourceSystems: List of source systems to filter by.
            listofSourceID: List of source IDs to filter by.

        Returns:
            Filtered list of sources.
        """
        sources = self.ingestConfiguration.collect()

        if not listofSourceSystems and not listofSourceID:
            return sources

        if listofSourceSystems:
            systems_set = set(listofSourceSystems)
            sources = [source for source in sources if source.system_code in systems_set]

        if listofSourceID:
            sourceid_set = set(listofSourceID)
            sources = [source for source in sources if source.SourceID in sourceid_set]

        return sources

    def validateTables(self, rawDF=None, sourceParams=None):
        """
        Validate tables by processing raw dataframes and saving them to the trusted stage.

        Args:
            rawDF: Raw dataframe to be validated.
            sourceParams: Additional parameters for source.
        """

        # TODO: add the ability to pass in a single raw datagrame and process that into trusted
        if not rawDF:
            for source in self.sources:
                if source["validation_enabled"]:
                    lakehouse_raw = FabricLakehouseLocation(
                        self.constants['LAKEHOUSE_RAW_STAGE_NAME'],
                        source["raw_workspace"],
                        source["raw_lakehouse"]
                    )
                    raw_destination_table = FabricTableLocation(source["destination_name"], lakehouse_raw)
                    df = self.fabricInterface.loadLatestDeltaTable(raw_destination_table)

                    lakehouse_trusted = FabricLakehouseLocation(
                        self.constants['LAKEHOUSE_TRUSTED_STAGE_NAME'],
                        source["trusted_workspace"],
                        source["trusted_lakehouse"]
                    )
                    trusted_destination_table = FabricTableLocation(source["destination_name"], lakehouse_trusted)

                    if self.constants['LOGGING_LEVEL'] != 'NONE':
                        # creates the first initial log in this section
                        assembler = LogAssembler(self.entity_log_stream, self.constants, source, "Processing", self.constants['LAKEHOUSE_TRUSTED_STAGE_NAME'])
                        newLog = assembler.createLog()
                        self.logger.updateAndQueueLog(newLog, None, self.entity_log_stream)

                    # check the save type (CDC or not)
                    if "cdc" not in source["trusted_savetype"].lower():
                        targetCount = self.fabricInterface.saveDeltaTable(
                            sourceDataFrame=df,
                            fabricTableLocation=trusted_destination_table,
                            savetype=source["trusted_savetype"],
                            primarykey=source["primary_key"]
                        )
                    else: #TODO: create a CDC function call
                        pass

                    # now log the save event.
                    if self.constants['LOGGING_LEVEL'] != 'NONE':
                        updated_log = {
                            "EndDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                            "LogDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                            "Status": "Completed", "SourceRows": df.count(), "TargetRows": targetCount
                        }
                        log = Log(self.entity_log_stream, updated_log)
                        self.logger.updateAndQueueLog(newLog, log, self.entity_log_stream)

                else: # if the validation is not enabled for the SourceID
                    print(f'Skipping SourceID: {source["SourceID"]} as it is disabled in the ingestion configuration.')
                    if self.constants['LOGGING_LEVEL'] in ['INFO', 'DEBUG']:
                        updated_log = {
                            "EndDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                            "LogDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                            "Status": "Skipped"
                        }
                        log = Log(self.entity_log_stream, updated_log)
                        self.logger.updateAndQueueLog(newLog, log, self.entity_log_stream)



    # TODO: Option to load only a single table or multiple (provided as a list)
    def loadTables(self):
        """
        Load tables from the sources, preprocess and save them to the raw stage.
        """
        for source in self.sources:
            print(f'Evaluating SourceID: {source["SourceID"]}')

            if source["ingestion_enabled"]:
                print(f'Ingestion enabled for SourceID: {source["SourceID"]} and ingestion started.')

                if source["source_type"] == 'FABRIC-TEXT':
                    connection = source["raw_workspace"] + ";" + source["raw_lakehouse"]
                elif source["source_type"] == 'FABRIC-TABLE':
                    connection = source["prelanding_workspace"] + ";" + source["prelanding_lakehouse"]
                else:
                    keyvaultConnection = KeyVault(
                        source["key_vault_name"], source["tenant_id"], source["client_id"],
                        source["client_secret"], source["secret_name"]
                    )
                    connection = keyvaultConnection.secretValue

                newDataSource = DataSource.getDataSourceType(connection, source, self.function)
                loaded_data = newDataSource.loadTable()

                lakehouse_raw = FabricLakehouseLocation(
                    self.constants['LAKEHOUSE_RAW_STAGE_NAME'],
                    source["raw_workspace"],
                    source["raw_lakehouse"]
                )
                raw_destination_table = FabricTableLocation(source["destination_name"], lakehouse_raw)

                if self.constants['LOGGING_LEVEL'] != 'NONE':
                    # creates the first initial log
                    assembler = LogAssembler(self.entity_log_stream, self.constants, source, "Processing", self.constants['LAKEHOUSE_RAW_STAGE_NAME'])
                    newLog = assembler.createLog()
                    self.logger.updateAndQueueLog(newLog, None, self.entity_log_stream)

                targetCount = self.fabricInterface.saveDeltaTable(
                    loaded_data,
                    raw_destination_table,
                    savetype=source["raw_savetype"],
                    primarykey=source["primary_key"]
                )

                if self.constants['LOGGING_LEVEL'] != 'NONE':
                    updated_log = {
                        "EndDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                        "LogDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                        "Status": "Completed", "SourceRows": loaded_data.count(), "TargetRows": targetCount
                    }
                    log = Log(self.entity_log_stream, updated_log)
                    self.logger.updateAndQueueLog(newLog, log, self.entity_log_stream)

            else:
                print(f'Skipping SourceID: {source["SourceID"]} as it is disabled in the ingestion configuration.')
                if self.constants['LOGGING_LEVEL'] in ['INFO', 'DEBUG']:
                    updated_log = {
                        "EndDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                        "LogDateTime": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                        "Status": "Skipped"
                    }
                    log = Log(self.entity_log_stream, updated_log)
                    self.logger.updateAndQueueLog(newLog, log, self.entity_log_stream)


class KeyVault:
    """
    Class for interacting with Azure Key Vault to retrieve secrets.
    """

    def __init__(self, keyvaultname, tenantid, clientid, clientsecret, secretName):
        """
        Initialize the KeyVault client.

        Args:
            keyvaultname: Name of the Key Vault.
            tenantid: Azure Tenant ID.
            clientid: Azure Client ID.
            clientsecret: Azure Client Secret.
            secretName: Name of the secret to retrieve.
        """
        credential = ClientSecretCredential(tenantid, clientid, clientsecret)
        vaultURL = f"https://{keyvaultname}.vault.azure.net"
        secretClient = SecretClient(vault_url=vaultURL, credential=credential)
        self.secretVal = secretClient.get_secret(secretName).value

    @property
    def secretValue(self):
        """
        Retrieve the secret value.

        Returns:
            Secret value from the Key Vault.
        """
        return self.secretVal
