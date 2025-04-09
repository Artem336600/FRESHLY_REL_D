document.getElementById('dataForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const inputData = document.getElementById('inputData').value.trim();
    if (!inputData) {
        showError('Пожалуйста, введите тему для поиска');
        return;
    }
    
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = `
        <div class="spinner-container">
            <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
        </div>
    `;
    
    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputData })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }

        displayResults(data);
    } catch (error) {
        showError('Произошла ошибка при обработке данных. Пожалуйста, попробуйте снова.');
        console.error('Error:', error);
    }
});

function showError(message) {
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = `
        <div class="error-container">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            <h5>Ошибка</h5>
            <p>${message}</p>
        </div>
    `;
}

function displayResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    let html = '';
    
    // Заголовок
    html += `<h2 class="mb-4 text-center">Результаты по теме: ${data.topic}</h2>`;
    
    // Факты
    if (data.facts) {
        html += `
            <div class="facts-section">
                <h3 class="facts-title">
                    <i class="bi bi-lightbulb me-2"></i>
                    Интересные факты
                </h3>
                <p>${data.facts.replace(/\n/g, '<br>')}</p>
            </div>
        `;
    }

    // Продукты по категориям
    if (data.products && data.products.length > 0) {
        data.products.forEach(category => {
            html += `
                <div class="category-section">
                    <div class="category-header">
                        <h4><i class="bi bi-tag me-2"></i>${category.category}</h4>
                    </div>
                    <p class="reason-text">${category.reason}</p>
                    <div class="product-cards">
            `;
            
            // Функция для извлечения данных продукта из строки
            function extractProductData(productText) {
                const productNameMatch = productText.match(/Продукт: (.*?)(?:\n|$)/);
                const costMatch = productText.match(/Стоимость: (.*?)(?:\n|$)/);
                const availabilityMatch = productText.match(/Наличие: (.*?)(?:\n|$)/);
                const categoryMatch = productText.match(/Категория БД: (.*?)(?:\n|$)/);
                const imageUrlMatch = productText.match(/Изображение: (.*?)(?:\n|$)/);
                
                return {
                    name: productNameMatch ? productNameMatch[1] : 'Название не найдено',
                    cost: costMatch ? costMatch[1] : 'Цена не указана',
                    availability: availabilityMatch ? availabilityMatch[1] : null,
                    category: categoryMatch ? categoryMatch[1] : null,
                    imageUrl: imageUrlMatch ? imageUrlMatch[1] : 'https://via.placeholder.com/300x200?text=Нет+изображения'
                };
            }
            
            category.items.forEach(productText => {
                const product = extractProductData(productText);
                html += `
                    <div class="product-card">
                        <img src="${product.imageUrl}" alt="${product.name}" class="product-image">
                        <div class="product-info">
                            <h5 class="product-name">${product.name}</h5>
                            <div class="product-price">${product.cost}</div>
                            ${product.availability ? `<div class="product-meta">Наличие: ${product.availability}</div>` : ''}
                            ${product.category ? `<div class="product-meta">Категория: ${product.category}</div>` : ''}
                        </div>
                    </div>
                `;
            });
            
            html += `
                    </div>
                </div>
            `;
        });
    } else {
        html += `
            <div class="text-center my-5">
                <i class="bi bi-search display-1 text-muted"></i>
                <p class="lead mt-3">Не найдено продуктов в базе данных для данной темы.</p>
            </div>
        `;
    }
    
    resultsContainer.innerHTML = html;
} 