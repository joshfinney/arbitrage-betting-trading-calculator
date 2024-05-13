document.addEventListener('DOMContentLoaded', () => {
    const fullscreenBtn = document.getElementById('fullscreen-btn');
    const resultContainer = document.querySelector('.result-container');
  
    // Toggle fullscreen mode
    fullscreenBtn.addEventListener('click', () => {
      resultContainer.classList.toggle('fullscreen');
      fullscreenBtn.textContent = resultContainer.classList.contains('fullscreen') ? 'Exit Fullscreen' : 'Toggle Fullscreen';
    });
  
    // Add input validation to all form inputs
    document.querySelectorAll('.form-input').forEach(input => {
      input.addEventListener('input', validateInput);
    });
  });
  
  /**
   * Adjust the numeric value of an input field by a specified amount.
   * @param {string} id - The ID of the input element.
   * @param {number} value - The amount to adjust the input value by.
   */
  const adjustValue = (id, value) => {
    const input = document.getElementById(id);
    const currentValue = parseFloat(input.value);
    const newValue = currentValue + value;
    if (!isNaN(newValue)) {
      input.value = newValue.toFixed(2);  // Keep two decimal places
    }
  };
  
  /**
   * Validate input to allow only numeric values with an optional decimal point.
   * @param {Event} event - The input event.
   */
  const validateInput = (event) => {
    const input = event.target;
    const value = input.value;
    if (!/^\d*\.?\d*$/.test(value)) {
      input.value = value.slice(0, -1);  // Remove last character if invalid
    }
  };
  
  /**
   * Copy text content to clipboard and show a tooltip.
   * @param {HTMLElement} element - The element containing the text to copy.
   */
  const copyToClipboard = (element) => {
    const text = element.innerText.trim();
    navigator.clipboard.writeText(text)
      .then(() => {
        const tooltip = element.querySelector('.tooltip');
        tooltip.classList.add('show');
        setTimeout(() => {
          tooltip.classList.remove('show');
        }, 1500);
      })
      .catch(err => {
        console.error('Failed to copy text to clipboard:', err);
      });
  };  