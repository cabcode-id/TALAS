function openForm(evt, formName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].classList.remove("active");
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].classList.remove("active");
  }
  document.getElementById(formName).classList.add("active");
  evt.currentTarget.classList.add("active");
}

// Articles form submission
document
  .getElementById("articlesForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    try {
      const response = await fetch("/insert-article", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      document.getElementById("responseJson").textContent = JSON.stringify(
        data,
        null,
        2
      );
    } catch (error) {
      document.getElementById("responseJson").textContent =
        "Error: " + error.message;
      console.error("Fetch error:", error);
    }
  });

// Title form submission
document
  .getElementById("titleForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    try {
      const response = await fetch("/insert-title", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      document.getElementById("responseJson").textContent = JSON.stringify(
        data,
        null,
        2
      );
    } catch (error) {
      document.getElementById("responseJson").textContent =
        "Error: " + error.message;
      console.error("Fetch error:", error);
    }
  });
