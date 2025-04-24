from typing import List
from mistralai import Mistral


class MistralOCR:
    def __init__(self, api_key: str, delete_after_ocr: bool = True):
        self.api_key = api_key
        self.delete_after_ocr = delete_after_ocr

    def ocr(self, filename) -> List[str]:
        file_id, pdf_url = self._upload_pdf(filename)
        ocr_response = self._run_ocr(pdf_url)
        if self.delete_after_ocr:
            self._delete_file(file_id)
        return [page.markdown for page in ocr_response.pages]

    def _upload_pdf(self, filename):
        with Mistral(api_key=self.api_key) as mistral:
            uploaded_pdf = mistral.files.upload(
                file={
                    "file_name": filename,
                    "content": open(filename, "rb"),
                },
                purpose="ocr",
            )
            signed_url = mistral.files.get_signed_url(file_id=uploaded_pdf.id)
            return uploaded_pdf.id, signed_url.url

    def _run_ocr(self, pdf_url):
        with Mistral(api_key=self.api_key) as mistral:
            ocr_response = mistral.ocr.process(
                model="mistral-ocr-latest",
                document={"type": "document_url", "document_url": pdf_url},
            )
            return ocr_response

    def _delete_file(self, file_id):
        with Mistral(api_key=self.api_key) as mistral:
            mistral.files.delete(file_id=file_id)
