class DownloadUtils {

    static downloadFile(filename, blob) {

        // create object url for blob
        const objectUrl = URL.createObjectURL(blob);

        // create hidden link element to download blob
        const link = document.createElement('a');
        link.href = objectUrl;
        link.download = filename;
        link.style.display = "none";
        document.body.append(link);

        // click link to download file in browser
        link.click();

        // link element is no longer needed
        link.remove();

        // revoke object url to clear memory
        setTimeout(() => URL.revokeObjectURL(objectUrl), 10000);

    }

}

export default DownloadUtils;
