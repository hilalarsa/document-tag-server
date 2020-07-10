1. get document
2. split the document into pdf and image
3. place pdf to pypdf to get text
4. if the pdf turns out to be an image screenshot, convert it into image format
5. place the image from split and pdf, to ocr to get text
6. remove empty space, symbols, and change to lowercase
# start of text check
Text checker is created to check every text inside the first array, with text on second param. It will ONLY return if the match similarities is above 80%
7. check each word for *judul*. split each judul's trigger word into individual word, compare both
8. if match with the first trigger word, count as match, save the judul
9. if no match found, append an "unknown" as judul
10. check each word for *nama_dosen*, loop each splitted nama dosen, until match. get nama, nidn, and nip.
# rule based
11. check if is_multiple is true, and dosen is more than 1:
    a. IF document is_multiple is true, bobot is rated down (nDosen-10 to 0)
    b. IF document is_multiple is false, bobot is the same for all dosen
12. Regex on nomor and tanggal
13. Output





CONSTRAINT
1. trigger word should not be duplicate
2. nama dosen should not be duplicate and shortened
3. output is highly based on image and scan quality

Afternote :
