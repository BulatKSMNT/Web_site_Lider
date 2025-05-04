document.addEventListener("DOMContentLoaded", function() {
  const hasErrors = document.querySelector('.form-errors') !== null;
  const hasMessages = document.querySelector('.messages') !== null;

  if (hasErrors) {
    const modal = new bootstrap.Modal(document.getElementById('myModal'));
    modal.show();

    if (hasErrors || hasMessages) {
      const modalElement = document.getElementById('myModal');
      document.getElementById('myModal').scrollIntoView({ behavior: 'smooth' });
      modalElement.addEventListener('hidden.bs.modal', function () {
        modal.hide();
      });
    }
  }
});