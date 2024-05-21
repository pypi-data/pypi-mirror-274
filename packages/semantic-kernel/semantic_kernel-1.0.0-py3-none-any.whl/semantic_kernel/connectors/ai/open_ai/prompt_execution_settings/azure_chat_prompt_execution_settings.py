import logging
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import AliasGenerator, ConfigDict, Field
from pydantic.alias_generators import to_camel, to_snake
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.open_ai_prompt_execution_settings import (
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.kernel_pydantic import KernelBaseModel

logger = logging.getLogger(__name__)


class AzureChatRequestBase(KernelBaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(validation_alias=to_camel, serialization_alias=to_snake),
        use_enum_values=True,
        extra="allow",
    )


class ConnectionStringAuthentication(AzureChatRequestBase):
    type: Annotated[Literal["ConnectionString", "connection_string"], AfterValidator(to_snake)] = "connection_string"
    connection_string: Optional[str] = None


class ApiKeyAuthentication(AzureChatRequestBase):
    type: Annotated[Literal["APIKey", "api_key"], AfterValidator(to_snake)] = "api_key"
    key: Optional[str] = None


class AzureEmbeddingDependency(AzureChatRequestBase):
    type: Annotated[Literal["DeploymentName", "deployment_name"], AfterValidator(to_snake)] = "deployment_name"
    deployment_name: Optional[str] = None


class DataSourceFieldsMapping(AzureChatRequestBase):
    title_field: Optional[str] = None
    url_field: Optional[str] = None
    filepath_field: Optional[str] = None
    content_fields: Optional[List[str]] = None
    vector_fields: Optional[List[str]] = None
    content_fields_separator: Optional[str] = "\n"


class AzureDataSourceParameters(AzureChatRequestBase):
    index_name: str
    index_language: Optional[str] = None
    fields_mapping: Optional[DataSourceFieldsMapping] = None
    in_scope: Optional[bool] = True
    top_n_documents: Optional[int] = 5
    semantic_configuration: Optional[str] = None
    role_information: Optional[str] = None
    filter: Optional[str] = None
    strictness: int = 3
    embedding_dependency: Optional[AzureEmbeddingDependency] = None


class AzureCosmosDBDataSourceParameters(AzureDataSourceParameters):
    authentication: Optional[ConnectionStringAuthentication] = None
    database_name: Optional[str] = None
    container_name: Optional[str] = None
    embedding_dependency_type: Optional[AzureEmbeddingDependency] = None


class AzureCosmosDBDataSource(AzureChatRequestBase):
    type: Literal["azure_cosmos_db"] = "azure_cosmos_db"
    parameters: AzureCosmosDBDataSourceParameters


class AzureAISearchDataSourceParameters(AzureDataSourceParameters):
    endpoint: Optional[str] = None
    query_type: Annotated[
        Literal["simple", "semantic", "vector", "vectorSimpleHybrid", "vectorSemanticHybrid"], AfterValidator(to_snake)
    ] = "simple"
    authentication: Optional[ApiKeyAuthentication] = None


class AzureAISearchDataSource(AzureChatRequestBase):
    type: Literal["azure_search"] = "azure_search"
    parameters: Annotated[dict, AzureAISearchDataSourceParameters]


DataSource = Annotated[Union[AzureAISearchDataSource, AzureCosmosDBDataSource], Field(discriminator="type")]


class ExtraBody(KernelBaseModel):
    data_sources: Optional[List[DataSource]] = None
    input_language: Optional[str] = Field(None, serialization_alias="inputLanguage")
    output_language: Optional[str] = Field(None, serialization_alias="outputLanguage")

    def __getitem__(self, item):
        return getattr(self, item)


class AzureChatPromptExecutionSettings(OpenAIChatPromptExecutionSettings):
    """Specific settings for the Azure OpenAI Chat Completion endpoint."""

    response_format: Optional[str] = None
    extra_body: Optional[Union[Dict[str, Any], ExtraBody]] = None
