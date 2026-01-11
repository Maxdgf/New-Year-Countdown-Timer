const copyTimeLeftDataButton = document.getElementById("copy_time_left_data");
const timeUntilNewYearField = document.getElementById("time_left_until_new_year_view");

function copyContent() {
    let contentToCopy = timeUntilNewYearField.textContent;
    navigator.clipboard.writeText(contentToCopy); // copy to clipboard
    console.info(contentToCopy, " recorded to clipboard.");
}

copyTimeLeftDataButton.onclick = copyContent; // set onclick function