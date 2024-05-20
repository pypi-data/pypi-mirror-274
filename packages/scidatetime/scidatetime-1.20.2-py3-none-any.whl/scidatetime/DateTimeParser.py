from .MdlDateTime import DateTime
import parsedatetime as pdt
pdt_cal = pdt.Calendar


class DateTimeParser:
    def parse(content: str) -> DateTime:
        ...
