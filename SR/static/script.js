document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript carregado e executado.");

  // Obter elemento de dados de funcionários
  const funcionariosDataElement = document.getElementById("funcionarios-data");
  let funcionariosSuperintendencias = {};

  if (funcionariosDataElement) {
    try {
      funcionariosSuperintendencias = JSON.parse(
        funcionariosDataElement.textContent || "{}"
      );
      console.log(funcionariosSuperintendencias);
    } catch (error) {
      console.error("Erro ao fazer parse do JSON:", error);
    }
  } else {
    console.error("Elemento 'funcionarios-data' não encontrado.");
  }

  if (typeof jQuery !== "undefined") {
    console.log("jQuery está carregado!");
    $(".select2").select2({
      width: "100%", // Ajusta a largura do Select2 para preencher o container
    });
  } else {
    console.error("jQuery não está carregado.");
  }

  // Função para atualizar superintendências
  window.atualizarSuperintendencia = function () {
    const keyUsersSelect = document.getElementById("key_users");
    const superintendenciasSelect =
      document.getElementById("superintendencias");

    if (!keyUsersSelect || !superintendenciasSelect) {
      console.error("Elementos de seleção não encontrados.");
      return;
    }

    // Limpar seleções atuais
    $(superintendenciasSelect).val(null).trigger("change");

    // Atualizar superintendências com base nos key users selecionados
    const selectedKeyUsers = Array.from(keyUsersSelect.selectedOptions).map(
      (option) => option.value
    );
    console.log("Usuários selecionados:", selectedKeyUsers);

    const newSuperIds = new Set();
    selectedKeyUsers.forEach((userId) => {
      const superId = funcionariosSuperintendencias[userId];
      if (superId) {
        newSuperIds.add(superId);
      }
    });

    // Atualizar as opções selecionadas no Select2
    $(superintendenciasSelect).val(Array.from(newSuperIds)).trigger("change");
    console.log("Superintendências selecionadas:", Array.from(newSuperIds));
  };

  // Função para verificar o estado dos checkboxes em cada projeto
  function checkProjectCheckboxesState() {
    const projectCards = document.querySelectorAll(".project-card");

    projectCards.forEach((card, index) => {
      const checkbox = card.querySelector(".toggle-completed");
      if (checkbox) {
        if (checkbox.checked) {
          console.log(`Checkbox for project ${index} is checked.`);
        } else {
          console.log(`Checkbox for project ${index} is not checked.`);
        }
      }
    });
  }

  // Verificar o estado inicial do checkbox
  checkProjectCheckboxesState();

  // Adicionar um evento para verificar o estado sempre que qualquer checkbox mudar
  const checkboxes = document.querySelectorAll(".toggle-completed");
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", checkProjectCheckboxesState);
  });

  function redirectToUpdate(projetoId) {
    const checkbox = document.getElementById(`show-completed-${projetoId}`);
    const showCompleted = checkbox.checked ? "on" : "off";
    const url =
      `{{ url_for('main.update', projeto_id='PROJETO_ID', show_completed='SHOW_COMPLETED') }}`
        .replace("PROJETO_ID", projetoId)
        .replace("SHOW_COMPLETED", showCompleted);
    window.location.href = url;
  }

  // Adicionar event listeners aos botões e formulário
  adicionarListeners();

  // Função de pesquisa
  const searchInput = document.getElementById("search-input");
  const projectCards = document.querySelectorAll(".project-card");

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = searchInput.value.toLowerCase();

      projectCards.forEach((card) => {
        const projectName = card
          .getAttribute("data-project-name")
          .toLowerCase();
        const projectTitle = card.querySelector("h3");
        if (projectName.includes(searchTerm)) {
          projectTitle.classList.add("highlight");
        } else {
          projectTitle.classList.remove("highlight");
        }
      });
    });
  }
});

function adicionarListeners() {
  const addTaskButton = document.getElementById("addTask");
  if (addTaskButton) {
    addTaskButton.addEventListener("click", addTask);
  }

  const addProblemButton = document.getElementById("addProblem");
  if (addProblemButton) {
    addProblemButton.addEventListener("click", addProblem);
  }

  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", validateForm);
  }
}

function addTask() {
  const table = document.getElementById("tasksTable");
  const row = table.insertRow();

  row.innerHTML = `
    <td><input type="text" name="tarefas[]" required></td>
    <td><input type="text" name="responsaveis[]" required></td>
    <td>
      <select name="status_tarefas[]" required>
        <option value="Concluída">Concluída</option>
        <option value="Replanejada">Replanejada</option>
        <option value="Planejada">Planejada</option>
        <option value="Em Andamento">Em Andamento</option>
        <option value="Prazo Vencido">Prazo Vencido</option>
        <option value="Em Replanejamento">Em Replanejamento</option>
      </select>
    </td>
    <td><input type="date" name="datas_inicio[]" required></td>
    <td><input type="date" name="datas_termino[]" required></td>
    <td><input type="date" name="datas_entrega_inicio[]" required></td>
    <td><input type="date" name="datas_entrega_fim[]" required></td>
    <td><input type="text" name="observacoes[]" required></td>
    <td><button type="button" onclick="removeTask(this)">Remover</button></td>
  `;
}

function removeTask(button) {
  const row = button.parentNode.parentNode;
  row.parentNode.removeChild(row);
}

function addProblem() {
  const table = document.getElementById("problemsTable");
  const row = table.insertRow();

  row.innerHTML = `
    <td>
      <select name="tipos[]">
        <option value="Problema">Problema</option>
        <option value="Risco">Risco</option>
      </select>
    </td>
    <td><input type="text" name="problemas[]"></td>
    <td><input type="text" name="impactos[]"></td>
    <td><input type="text" name="acoes_corretivas[]"></td>
    <td><input type="text" name="agentes_solucao[]"></td>
    <td><input type="date" name="datas_alvo_solucao[]"></td>
    <td><input type="text" name="coordenadores_agente_solucao[]"></td>
    <td><input type="text" name="status_problemas[]"></td>
    <td><button type="button" onclick="removeProblem(this)">Remover</button></td>
  `;
}

function removeProblem(button) {
  const row = button.parentNode.parentNode;
  row.parentNode.removeChild(row);
}

function validateForm(event) {
  const tasks = document.querySelectorAll('input[name="tarefas[]"]');
  if (tasks.length === 0) {
    alert("Por favor, adicione pelo menos uma tarefa.");
    event.preventDefault();
  }
}
