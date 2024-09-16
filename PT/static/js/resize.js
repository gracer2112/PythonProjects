document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript carregado e executado.");

  // Inicializa o Select2
  const selects = document.querySelectorAll(
    'select[name="responsavel"], select[name="coordenador"]'
  );
  selects.forEach((select) => {
    $(select)
      .select2({
        placeholder: "Selecione um funcionário",
        allowClear: true,
      })
      .on("select2:unselect", function (e) {
        const role = e.target.name;
        const emailElement = document.querySelector(
          `input[name="email_${role}"]`
        );
        console.log("Selecione um funcionario");
        if (emailElement) {
          emailElement.value = "";
        }
      });
  });

  // Define os e-mails com base nas seleções iniciais
  updateEmail("responsavel");
  updateEmail("coordenador");

  // Atualiza os emails quando a seleção muda
  const responsavelSelect = document.getElementById("responsavel");
  const coordenadorSelect = document.getElementById("coordenador");

  if (responsavelSelect) {
    responsavelSelect.addEventListener("change", function () {
      updateEmail("responsavel");
    });
  }

  if (coordenadorSelect) {
    coordenadorSelect.addEventListener("change", function () {
      updateEmail("coordenador");
    });
  }

  const today = new Date().toISOString().split("T")[0];
  const dataInicioElement = document.getElementById("data_inicio_planejada");
  const dataFimElement = document.getElementById("data_fim_planejada");

  if (dataInicioElement) {
    dataInicioElement.value = today;
  }

  if (dataFimElement) {
    dataFimElement.value = today;
  }

  const table = document.querySelector("table");
  if (table) {
    const cols = table.querySelectorAll("th");
    let isResizing = false;
    let lastDownX = 0;
    let th = null;

    cols.forEach((col) => {
      col.classList.add("resizable");
      col.addEventListener("mousedown", function (e) {
        th = col;
        isResizing = true;
        lastDownX = e.clientX;
      });
    });

    document.addEventListener("mousemove", function (e) {
      if (!isResizing) return;
      const diffX = e.clientX - lastDownX;
      th.style.width = th.offsetWidth + diffX + "px";
      lastDownX = e.clientX;
    });

    document.addEventListener("mouseup", function () {
      isResizing = false;
    });
  }

  // Adiciona funcionalidade de filtro
  const filters = [
    "filterActions",
    "filterID",
    "filterSeq",
    "filterDependencia",
    "filterCenario",
    "filterModulo",
    "filterCasoTeste",
    "filterInfoTeste",
    "filterPassos",
    "filterResultado",
    "filterStatus",
    "filterResponsavel",
    "filterEmaildoResponsavel",
    "filterCoordenador",
    "filterEmaildoCoordenador",
    "filterDataInícioPlanejada",
    "filterDataFimPlanejada",
    "filterDataInicioRealizada",
    "filterDataFimRealizada",
    "filterObservacao",
  ];

  function clearFilters() {
    // Limpa os valores dos inputs de filtro
    document.querySelectorAll(".filter-input").forEach((input) => {
      input.value = ""; // Limpa o valor do input
    });

    // Remove filtros do localStorage
    filters.forEach((filterId) => {
      localStorage.removeItem(filterId); // Remova cada filtro armazenado
    });

    // Atualiza a tabela para remover os filtros aplicados
    applyFilters();
  }

  // Associa a função ao botão "Limpar Filtros"
  const clearFiltersButton = document.getElementById("clear-filters-button");
  if (clearFiltersButton) {
    clearFiltersButton.addEventListener("click", function (event) {
      event.preventDefault(); // Evita o envio do formulário
      clearFilters(); // Chama a função para limpar filtros
      document.getElementById("clear-filters-form").submit(); // Envia o formulário para recarregar a página
    });
  }

  function applyFilters() {
    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach((row) => {
      let isVisible = true;
      filters.forEach((filterId, index) => {
        const filterInput = document.getElementById(filterId);
        if (filterInput) {
          const filterValue = filterInput.value.toLowerCase();
          const cell = row.querySelectorAll("td")[index];
          if (cell) {
            const text = cell.textContent || cell.innerText;
            if (!text.toLowerCase().includes(filterValue)) {
              isVisible = false;
            }
          }
        }
      });
      row.style.display = isVisible ? "" : "none";
    });
  }

  filters.forEach((filterId) => {
    const filterInput = document.getElementById(filterId);
    if (filterInput) {
      // Carregar filtros do localStorage ao carregar a página
      const savedValue = localStorage.getItem(filterId);
      if (savedValue) {
        filterInput.value = savedValue;
      }

      filterInput.addEventListener("input", function () {
        localStorage.setItem(filterId, this.value);
        applyFilters();
      });
    }
  });

  // Aplicar filtros após carregar os valores
  applyFilters();

  const generateExcelButton = document.getElementById("generateExcel");
  if (generateExcelButton) {
    generateExcelButton.addEventListener("click", function () {
      const rows = document.querySelectorAll("table tbody tr");
      const data = [];

      rows.forEach((row) => {
        if (row.style.display !== "none") {
          const cells = row.querySelectorAll("td");
          const rowData = Array.from(cells)
            .slice(1)
            .map((cell) => cell.textContent.trim());
          data.push(rowData);
        }
      });

      fetch(`/generate_excel/${project_id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ data }),
      })
        .then((response) => response.blob())
        .then((blob) => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "test_cases.xlsx";
          document.body.appendChild(a);
          a.click();
          a.remove();
        })
        .catch((error) => console.error("Error:", error));
    });
  }

  const projectFilter = document.getElementById("project_filter");
  if (projectFilter) {
    projectFilter.addEventListener("change", function () {
      if (this.value === "") {
        clearFilters();
        clearTable();
      }
    });
  }

  function clearTable() {
    const tableBody = document.querySelector("table tbody");
    if (tableBody) {
      tableBody.innerHTML = ""; // Remove todas as linhas da tabela
    }
  }

  // Lógica para o upload de casos de teste
  const uploadForm = document.getElementById("uploadForm");
  if (uploadForm) {
    uploadForm.addEventListener("submit", function (event) {
      event.preventDefault();
      console.log("Ativei o PreventDefault");
      document.getElementById("progress").style.display = "block";

      fetch(uploadForm.action, {
        method: "POST",
        body: new FormData(uploadForm),
      })
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("progress").style.display = "none";
          $("#uploadModal").modal("hide");
          if (data.success) {
            Swal.fire({
              icon: "success",
              title: "Sucesso!",
              text: "Casos de teste criados com sucesso!",
            }).then(() => {
              window.location.href = "{{ url_for('index') }}";
            });
          } else {
            Swal.fire({
              icon: "error",
              title: "Erro",
              text: data.message,
            });
          }
        })
        .catch((error) => {
          document.getElementById("progress").style.display = "none";
          Swal.fire({
            icon: "error",
            title: "Erro",
            text: "Erro ao processar o arquivo.",
          });
        });
    });
  }
});

// Função para atualizar o campo de e-mail quando um funcionário é selecionado
window.updateEmail = function (role) {
  const selectElement = document.querySelector(`select[name="${role}"]`);
  if (selectElement) {
    const emailElement = document.querySelector(`input[name="email_${role}"]`);
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    if (selectedOption) {
      console.log("update email");

      emailElement.value = selectedOption.getAttribute("data-email");
    }
  }
};
