// Adicione aqui qualquer script JavaScript necessário para o seu projeto
document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript carregado e funcionando.");

  document.getElementById("project_id").addEventListener("change", function () {
    document.getElementById("project_id").disabled = true;
    document.getElementById("project_search").disabled = true;
    document.getElementById("change_project").style.display = "inline";
  });
});

function searchProjects() {
  const query = document.getElementById("project_search").value;
  fetch(`/search_projects?query=${query}`)
    .then((response) => response.json())
    .then((data) => {
      const projectSelect = document.getElementById("project_id");
      projectSelect.innerHTML = ""; // Limpa as opções atuais

      // Adiciona uma opção vazia
      const emptyOption = document.createElement("option");
      emptyOption.value = "";
      emptyOption.textContent = "Selecione um Projeto";
      projectSelect.appendChild(emptyOption);

      // Adiciona as novas opções baseadas na busca
      data.forEach((project) => {
        const option = document.createElement("option");
        option.value = project.id;
        option.textContent = `${project.id} - ${project.name}`;
        projectSelect.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching projects:", error));
}

function changeProject() {
  document.getElementById("project_id").disabled = false;
  document.getElementById("project_search").disabled = false;
  document.getElementById("change_project").style.display = "none";
}

function captureAndDisableProjectId() {
  var projectIdSelect = document.getElementById("project_id");
  var hiddenProjectId = document.getElementById("hidden_project_id");

  // Captura o valor selecionado
  hiddenProjectId.value = projectIdSelect.value;

  // Desabilita o combo box
  projectIdSelect.disabled = true;
}
