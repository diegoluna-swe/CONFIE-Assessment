# Dependencies
from typing import Literal
from pydantic import BaseModel, Field
class TranscriptEvaluation(BaseModel):
    c1_greeting: Literal[0, 5, 10] = Field(description="Score for C1. Greeting and Identification."
    )
    c2_needs_discovery: Literal[0, 5, 10] = Field(description="Score for C2. Needs Discovery."
    )
    c3_compliance: Literal[0, 5, 10] = Field(description="Score for C3. Compliance and Disclosures."
    )
    c4_resolution: Literal[0, 5, 10] = Field(description="Score for C4. Resolution and Next Steps."
    )
    c5_professionalism: Literal[0, 5, 10] = Field(description="Score for C5. Professionalism and Call Control."
    )

    @property
    def total_score(self) -> int:
        return (
            self.c1_greeting
            + self.c2_needs_discovery
            + self.c3_compliance
            + self.c4_resolution
            + self.c5_professionalism
        )