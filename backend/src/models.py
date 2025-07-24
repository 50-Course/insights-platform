from sqlmodel import Field, SQLModel


class Insight(SQLModel, table=True):
    """
    Represents an AI-generated insight for a file.

    Attributes:
        id (int): Unique identifier for the insight.
        file_id (int): Identifier of the file associated with the insight.
        title (str): Title of the insight.
        description (str): Description of the insight.
        confidence_score (float): Confidence score of the insight.
        reference_rows (list[int]): List of row indices that the insight references.
    """

    id: int = Field(default=None, primary_key=True)
    file_id: int = Field(index=True, nullable=False)
    title: str = Field(max_length=255, nullable=False)
    description: str = Field(max_length=1000, nullable=False)
    confidence_score: float = Field(ge=0.0, le=1.0, nullable=False)
    reference_rows: list[int] = Field(default_factory=list, nullable=False)
