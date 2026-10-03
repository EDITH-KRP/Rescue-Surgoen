document.addEventListener('DOMContentLoaded', () => {
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
            navbar.style.padding = '0.5rem 2rem';
        } else {
            navbar.style.boxShadow = 'none';
            navbar.style.padding = '1rem 2rem';
        }
    });

    const API_BASE_URL = 'http://localhost:8000/api';

    // Fetch Impact Stats
    async function loadImpactStats() {
        try {
            const response = await fetch(`${API_BASE_URL}/impact`);
            const data = await response.json();
            
            if (data && !data.error) {
                document.querySelector('.counter[data-target="500"]').setAttribute('data-target', data.animals_helped || 500);
                document.querySelector('.counter[data-target="300"]').setAttribute('data-target', data.medical_treatments || 300);
                document.querySelector('.counter[data-target="150"]').setAttribute('data-target', data.successful_recoveries || 150);
                document.querySelector('.counter[data-target="50"]').setAttribute('data-target', data.rescue_operations || 50);
            }
        } catch (error) {
            console.error('Error fetching impact stats:', error);
        }
    }

    // Number Counter Animation
    const counters = document.querySelectorAll('.counter');
    const speed = 200; // The lower the slower

    const animateCounters = () => {
        counters.forEach(counter => {
            const updateCount = () => {
                const target = +counter.getAttribute('data-target');
                const count = +counter.innerText;
                const inc = target / speed;

                if (count < target) {
                    counter.innerText = Math.ceil(count + inc);
                    setTimeout(updateCount, 1);
                } else {
                    counter.innerText = target;
                }
            };
            
            // Check if element is in viewport
            const rect = counter.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom >= 0 && counter.innerText === '0') {
                updateCount();
            }
        });
    };

    // Initialize Impact Stats
    loadImpactStats().then(() => {
        window.addEventListener('scroll', animateCounters);
        animateCounters(); // Trigger on load if in view
    });

    // Fetch Animals
    async function loadAnimals() {
        try {
            const response = await fetch(`${API_BASE_URL}/animals`);
            const data = await response.json();
            
            if (data && !data.error) {
                const container = document.getElementById('animals-container');
                container.innerHTML = ''; // Clear placeholders
                
                data.forEach(animal => {
                    const iconMap = { 'dogs': 'fa-dog', 'cats': 'fa-cat', 'wildlife': 'fa-leaf' };
                    const icon = iconMap[animal.type] || 'fa-paw';
                    const statusClass = animal.status.toLowerCase().includes('recover') ? 'recovering' : 'rescued';

                    container.innerHTML += `
                        <div class="animal-card" data-category="${animal.type}">
                            <div class="animal-img placeholder-img"><i class="fa-solid ${icon}"></i></div>
                            <div class="animal-info">
                                <h3>${animal.name}</h3>
                                <span class="status ${statusClass}">${animal.status}</span>
                                <p>${animal.description}</p>
                                <a href="#" class="btn btn-outline btn-small">View Story</a>
                            </div>
                        </div>
                    `;
                });
            }
        } catch (error) {
            console.error('Error fetching animals:', error);
        }
    }

    loadAnimals();
});
