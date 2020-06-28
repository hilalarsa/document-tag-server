# import re

# text = ["27 september 2019", "27 sept 2019","27/09/97", "27/09/1997", "27-09-97", "27-09-1997"]

# pattern = "(([0-9])|([0-2][0-9])|([3][0-1]))[-/ ](jan|feb|mar|apr|may|jun|jul|aug|sept|sep|okt|nov|des|januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)[-/ ]\d{4}"
# for item in text:
#     prog = re.compile(pattern)
#     result = prog.match(item)
#     if result:
#         print result.group(0)
        # return result.group(0)