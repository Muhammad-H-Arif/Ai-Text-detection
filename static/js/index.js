const Text_Area = document.getElementById("text");
const File_Area = document.getElementById("file");
const Submit_Button = document.getElementById("submit");

File_Area.addEventListener("change", () => {
    // Disable text area if a file is selected
    Text_Area.disabled = File_Area.files.length > 0;
});

Text_Area.addEventListener("input", () => {
    // Disable file input if text is entered
    File_Area.disabled = Text_Area.value.length > 0;
    if (Text_Area.value.length > 0) {
        File_Area.title = "Please remove the text to enable the file upload";
    } else {
        File_Area.title = ""; // Clear the title when text area is empty
    }
});

const form = document.getElementById("form");
const Status = document.getElementById("Status");

form.addEventListener("submit", function(event) {
    Status.innerHTML = "Submitting...";
});

