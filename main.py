import json
from pydantic import BaseModel

class Annotation(BaseModel):
    span: dict
    index: int
    alignment_index: list = []
    
class root_text_manifestation_critical(BaseModel):
    metadata: dict
    annotation: list
    content: str

if __name__ == "__main__":
    with open("6_root_commentary_bo.txt", "r") as f:
        text = f.read()
    
    start = 0
    validate_start_end = []
    annotation = []
    pointer = 1
    string = ""
    cnt = 0
    for text in text.split("\n"):
        cnt += 1
        string += text + "\\n"
        end = start + len(text)
        validate_start_end.append({"start": start, "end": end})
        print(text, start, end, len(text))
        annotation.append(
            Annotation(
                span={"start": start, "end": end},
                index=pointer,
                alignment_index=[]
            )
        )
        start = end + 1
        pointer += 1
    
    import asyncio

    async def write_string():
        with open("string.txt", "w", encoding="utf-8") as f:
            await asyncio.to_thread(f.write, string)
    asyncio.run(write_string())
    async def write_annotation():
        with open("annotation.json", "w", encoding="utf-8") as f:
            await asyncio.to_thread(json.dump, [a.dict() for a in annotation], f, ensure_ascii=False, indent=2)

    asyncio.run(write_annotation())