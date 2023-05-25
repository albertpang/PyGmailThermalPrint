class ImageProcessing():
    def __init__(self) -> None:
        self.read_body()
        self.read_attachment()
        

# def triggerEmail():
# Default Setup of Email
def convertGrey(imageLocation):
    originalImage = "eakins.jpg"
    img = Image.open(originalImage)
    blurImage = img.filter(ImageFilter.BLUR)
    greyImage = blurImage.convert("1")
    greyImage.show()


# def clean(fileName) -> str:
#     return "FOLDER"

# def download_attachment(emailPart):
#     fileName = emailPart.get_filename()
#     if fileName:
#         folderName = clean(fileName)
#         if not os.path.isdir(fileName):
#             filePath = os.path.join(folderName,fileName)
#             open(filePath, "wb").write(emailPart.get_payload(decode=True))