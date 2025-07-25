console.log("Javascript chargé");

document.querySelectorAll('.edit-btn').forEach(btn => {
  btn.addEventListener('click', function (e) {
    e.preventDefault();
    const data = JSON.parse(this.dataset.prof);
    const id = this.dataset.id;

    document.getElementById("prof-id").value = id;
    document.getElementById("nom").value = data.nom;
    document.getElementById("matieres").value = data.matieres;
    document.getElementById("max_heures").value = data.max_heures;

    for (const day in data.disponibilites) {
      document.querySelector(`input[name="${day}_start"]`).value = data.disponibilites[day].start;
      document.querySelector(`input[name="${day}_end"]`).value = data.disponibilites[day].end;
    }

    window.scrollTo(0, 0);
  });
});