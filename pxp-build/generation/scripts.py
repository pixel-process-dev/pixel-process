script_flipbook = """```{=html}
<script>
let current = 0;

function updateFlipbook() {
  document.getElementById("flip-img").src = flipData[current].src;
  document.getElementById("flip-caption").textContent = flipData[current].caption;
}

function nextImage() {
  current = (current + 1) % flipData.length;
  updateFlipbook();
}

function prevImage() {
  current = (current - 1 + flipData.length) % flipData.length;
  updateFlipbook();
}

document.addEventListener("DOMContentLoaded", updateFlipbook);
</script>
```"""

script_toggle_all = """```{=html}
<script>
function toggleAll() {
  const detailsList = document.querySelectorAll("details");
  const allOpen = Array.from(detailsList).every(d => d.open);
  detailsList.forEach(d => d.open = !allOpen);
}
</script>
```"""

script_sidebar_toggle = """```{=html}
<script>
  const sidebar = document.getElementById('quarto-sidebar');
  const toggle = document.getElementById('sidebarToggle');

  toggle?.addEventListener('click', () => {
    sidebar.classList.toggle('d-none');
  });
</script>
```"""

sidebar_toggle_html = """<button id="sidebarToggle" class="btn btn-sm" aria-label="Toggle sidebar"
  style="position: fixed; top: 1rem; left: 1rem; z-index: 1050;">
  <i class="bi bi-layout-sidebar-inset"></i>
</button>"""


enable_thebe_script="""<script>
  const button = document.getElementById("enable-thebe");
  const status = document.getElementById("thebe-status");

  function updateStatus(message, color = "#555") {
    status.textContent = `Thebe: ${message}`;
    status.style.color = color;
  }

  button.addEventListener("click", () => {
    updateStatus("Loading...", "#999");

    if (window.thebelab) {
      thebelab.bootstrap();
      updateStatus("Active", "green");
      button.disabled = true;
      button.textContent = "✅ Interactivity Enabled";
    } else {
      updateStatus("Error: Thebe not loaded", "red");
    }
  });
</script>
"""
