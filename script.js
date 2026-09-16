/* ============================================================
   Movie Ticket Booking & Management System
   Interactive JavaScript Utilities & Real-Time Logic
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
    console.log("🎬 Movie Booking Interactive Engine Loaded!");

    // ============================================================
    // 1. DYNAMIC TICKET PRICE CALCULATOR & VISUAL SEAT GRID
    // ============================================================
    const seatTypeSelect = document.getElementById("seat_type");
    const ticketsInput = document.getElementById("tickets");
    const totalDisplay = document.getElementById("total_amount_display");
    const seatGridContainer = document.getElementById("interactiveSeatGrid");

    function calculateTotal() {
        if (!seatTypeSelect || !ticketsInput || !totalDisplay) return;

        const seatType = seatTypeSelect.value;
        const tickets = parseInt(ticketsInput.value) || 1;

        // Regular = ₹150, Premium = ₹250
        const pricePerTicket = (seatType === "Premium") ? 250 : 150;
        const totalAmount = tickets * pricePerTicket;

        totalDisplay.textContent = `₹${totalAmount}`;
    }

    if (seatTypeSelect && ticketsInput && totalDisplay) {
        seatTypeSelect.addEventListener("change", calculateTotal);
        ticketsInput.addEventListener("input", function() {
            updateSeatGridFromInput();
            calculateTotal();
        });
        calculateTotal();
    }

    // Build Visual Interactive Seats Grid if Container Exists
    if (seatGridContainer) {
        const rows = ['A', 'B', 'C', 'D'];
        const cols = 8;
        let selectedSeats = [];

        seatGridContainer.innerHTML = '';
        rows.forEach((row, rowIndex) => {
            for (let c = 1; c <= cols; c++) {
                const seatId = `${row}${c}`;
                const seatEl = document.createElement('div');
                seatEl.className = 'seat';
                seatEl.textContent = seatId;
                seatEl.dataset.seatId = seatId;

                // Mark some initial seats as booked for realism
                if ((rowIndex === 0 && c === 3) || (rowIndex === 1 && c === 4)) {
                    seatEl.classList.add('booked');
                    seatEl.title = 'Already Booked';
                } else {
                    seatEl.addEventListener('click', function () {
                        toggleSeatSelection(seatEl, seatId);
                    });
                }
                seatGridContainer.appendChild(seatEl);
            }
        });

        function toggleSeatSelection(seatEl, seatId) {
            if (seatEl.classList.contains('selected')) {
                seatEl.classList.remove('selected');
                selectedSeats = selectedSeats.filter(id => id !== seatId);
            } else {
                const currentTicketLimit = parseInt(ticketsInput.value) || 1;
                // If limit reached, select seat by updating count
                if (selectedSeats.length >= 10) {
                    showToast("Maximum 10 seats allowed per booking!");
                    return;
                }
                seatEl.classList.add('selected');
                selectedSeats.push(seatId);
            }

            // Sync ticket input value with selected seats count
            if (selectedSeats.length > 0) {
                ticketsInput.value = selectedSeats.length;
            }
            calculateTotal();
        }

        function updateSeatGridFromInput() {
            const count = parseInt(ticketsInput.value) || 1;
            const allSeats = Array.from(seatGridContainer.querySelectorAll('.seat:not(.booked)'));
            
            // Clear current selections
            allSeats.forEach(s => s.classList.remove('selected'));
            selectedSeats = [];

            // Auto-select top N seats
            for (let i = 0; i < Math.min(count, allSeats.length); i++) {
                allSeats[i].classList.add('selected');
                selectedSeats.push(allSeats[i].dataset.seatId);
            }
        }

        // Initialize top 2 seats selected by default
        updateSeatGridFromInput();
    }

    // ============================================================
    // 2. REAL-TIME SEARCH & GENRE FILTER (Movies Page)
    // ============================================================
    const movieSearchInput = document.getElementById("movieSearchInput");
    const genreTabs = document.querySelectorAll(".genre-tab");
    const movieCards = document.querySelectorAll(".movie-card");

    let currentGenre = "All";
    let searchQuery = "";

    function filterMovies() {
        if (!movieCards.length) return;

        movieCards.forEach(card => {
            const title = card.querySelector(".movie-title")?.textContent.toLowerCase() || "";
            const genre = card.dataset.genre?.toLowerCase() || "";

            const matchesGenre = (currentGenre === "All" || genre.includes(currentGenre.toLowerCase()));
            const matchesSearch = title.includes(searchQuery) || genre.includes(searchQuery);

            if (matchesGenre && matchesSearch) {
                card.style.display = "flex";
            } else {
                card.style.display = "none";
            }
        });
    }

    if (genreTabs.length) {
        genreTabs.forEach(tab => {
            tab.addEventListener("click", function () {
                genreTabs.forEach(t => t.classList.remove("active"));
                this.classList.add("active");
                currentGenre = this.dataset.genre;
                filterMovies();
            });
        });
    }

    if (movieSearchInput) {
        movieSearchInput.addEventListener("input", function () {
            searchQuery = this.value.trim().toLowerCase();
            filterMovies();
        });
    }

    // ============================================================
    // 3. INTERACTIVE MOVIE PREVIEW MODAL
    // ============================================================
    const modalBackdrop = document.getElementById("movieModal");
    const modalCloseBtn = document.getElementById("modalCloseBtn");
    const modalTitle = document.getElementById("modalTitle");
    const modalGenre = document.getElementById("modalGenre");
    const modalLanguage = document.getElementById("modalLanguage");
    const modalDuration = document.getElementById("modalDuration");
    const modalRating = document.getElementById("modalRating");
    const modalBookBtn = document.getElementById("modalBookBtn");

    document.querySelectorAll(".btn-preview-movie").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const card = this.closest(".movie-card");
            if (!card || !modalBackdrop) return;

            modalTitle.textContent = card.dataset.title;
            modalGenre.textContent = card.dataset.genre;
            modalLanguage.textContent = card.dataset.language;
            modalDuration.textContent = card.dataset.duration;
            modalRating.textContent = `★ ${card.dataset.rating} / 10`;
            modalBookBtn.href = `/book?movie_id=${card.dataset.id}`;

            modalBackdrop.classList.add("active");
        });
    });

    if (modalCloseBtn) {
        modalCloseBtn.addEventListener("click", function () {
            modalBackdrop.classList.remove("active");
        });
    }

    if (modalBackdrop) {
        modalBackdrop.addEventListener("click", function (e) {
            if (e.target === modalBackdrop) {
                modalBackdrop.classList.remove("active");
            }
        });
    }

    // ============================================================
    // 4. INTERACTIVE STAR RATING WIDGET (Reviews Page)
    // ============================================================
    const starSpans = document.querySelectorAll(".star-rating-input span");
    const ratingValueInput = document.getElementById("rating_value");
    const ratingFeedback = document.getElementById("rating_feedback");

    const ratingDescriptions = {
        "1": "1 Star — 😞 Poor",
        "2": "2 Stars — 😐 Fair",
        "3": "3 Stars — 🙂 Good",
        "4": "4 Stars — 😊 Very Good",
        "5": "5 Stars — 🤩 Excellent & Highly Recommended!"
    };

    if (starSpans.length && ratingValueInput) {
        starSpans.forEach((star, index) => {
            // Hover effect
            star.addEventListener("mouseenter", function () {
                const hoverVal = this.dataset.value;
                highlightStars(hoverVal);
                if (ratingFeedback) ratingFeedback.textContent = ratingDescriptions[hoverVal];
            });

            // Click selection
            star.addEventListener("click", function () {
                const selectedVal = this.dataset.value;
                ratingValueInput.value = selectedVal;
                highlightStars(selectedVal);
                if (ratingFeedback) ratingFeedback.textContent = ratingDescriptions[selectedVal];
                showToast(`Rating set to ${selectedVal} Stars!`);
            });
        });

        const ratingContainer = document.querySelector(".star-rating-input");
        if (ratingContainer) {
            ratingContainer.addEventListener("mouseleave", function () {
                const currentVal = ratingValueInput.value || "5";
                highlightStars(currentVal);
                if (ratingFeedback) ratingFeedback.textContent = ratingDescriptions[currentVal];
            });
        }

        function highlightStars(val) {
            starSpans.forEach(s => {
                if (parseInt(s.dataset.value) <= parseInt(val)) {
                    s.style.color = "#ffb400";
                } else {
                    s.style.color = "#4a4e5d";
                }
            });
        }
    }

    // ============================================================
    // 5. TOAST NOTIFICATION SYSTEM
    // ============================================================
    function showToast(message) {
        let toast = document.getElementById("toastNotification");
        if (!toast) {
            toast = document.createElement("div");
            toast.id = "toastNotification";
            toast.className = "toast-notification";
            document.body.appendChild(toast);
        }
        toast.textContent = message;
        toast.classList.add("show");
        setTimeout(() => {
            toast.classList.remove("show");
        }, 3000);
    }

    // Copy Booking ID functionality
    document.querySelectorAll(".btn-copy-id").forEach(btn => {
        btn.addEventListener("click", function () {
            const id = this.dataset.bookingId;
            navigator.clipboard.writeText(id).then(() => {
                showToast(`Copied Booking ID #${id} to clipboard!`);
            });
        });
    });
});
