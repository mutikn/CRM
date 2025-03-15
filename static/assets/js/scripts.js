"use strict";

function onScanSuccess(decodedText) {
  document.getElementById("result").innerText = "Scanned QR: " + decodedText;
  sendToServer(decodedText);
  html5QrCode
    .stop()
    .then(() => {
      console.log("QR code scanning stopped.");
    })
    .catch((err) => {
      console.error("Failed to stop scanning:", err);
    });
}

let html5QrCode = new Html5Qrcode("reader");
Html5Qrcode.getCameras()
  .then((devices) => {
    if (devices && devices.length) {
      // Find the front camera
      const frontCamera = devices.find((device) =>
        device.label.toLowerCase().includes("front")
      );
      const cameraId = frontCamera ? frontCamera.id : devices[0].id;
      html5QrCode
        .start(
          cameraId,
          {
            fps: 30,
            qrbox: 150,
          },
          onScanSuccess
        )
        .catch((err) => {
          console.error("Failed to start scanning:", err);
        });
    }
  })
  .catch((err) => {
    console.error("Failed to get cameras:", err);
  });

function getCSRFToken() {
  let tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
  return tokenElement ? tokenElement.value : "";
}

function sendToServer(qrData) {
  let jsonData = { username: qrData.trim() };

  console.log("Sending data:", jsonData);

  fetch("https://lifedocit.pl/api/attendance/scan_qr/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    credentials: "include",
    body: JSON.stringify(jsonData),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Server response:", data);
      let resultElement = document.getElementById("result");
      let resultTitle = document.getElementById("headTitle");

      if (data.message === "Checked-out" || data.message === "Checked-in") {
        resultElement.innerText = "Access granted";
        resultElement.style.color = "green";
        resultTitle.innerText = data.message;
        resultTitle.style.color = "green";
      } else if (data.message === "Today has already been logged in and out") {
        resultElement.innerText = "Access denied";
        resultElement.style.color = "red";
        resultTitle.innerText = data.message;
        resultTitle.style.color = "red";
      } else {
        resultElement.innerText = "Access denied";
        resultElement.style.color = "red";
        resultTitle.innerText = "You are not registered";
        resultTitle.style.color = "red";
      }

      setTimeout(() => {
        location.reload();
      }, 3000);
    })
    .catch((error) => console.error("Error:", error));
}
