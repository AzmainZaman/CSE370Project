document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('#login-form');
    const logoutButton = document.getElementById('logout-button');

    // -----------------------------------------------------------------------------
    // Centralized Authenticated Fetch (Cookie-based)
    // -----------------------------------------------------------------------------
    function authFetch(url, options = {}) {
        // We do NOT read localStorage anymore — the browser sends the JWT cookie automatically.
        options.headers = {
            ...options.headers,
            'Content-Type': 'application/json'
        };

        return fetch(url, options).then(response => {
            if (!response.ok) {
                // If the server returns a 401, that usually means no valid JWT cookie or session has expired
                if (response.status === 401) {
                    alert('Session expired or unauthorized. Please log in again.');
                    // Redirect to login page if we’re not already there
                    if (window.location.pathname !== '/auth/login') {
                        window.location.href = '/auth/login';
                    }
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        });
    }

    // -----------------------------------------------------------------------------
    // Login Handler
    // -----------------------------------------------------------------------------
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.querySelector('#email').value;
            const password = document.querySelector('#password').value;

            // Send credentials to the server (cookie is set on successful login)
            fetch('/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            })
            .then(response => {
                // If there's an HTTP error (like 401), handle it
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // The server has set the JWT cookie in the response headers
                    // We just do a front-end redirect based on the user role
                    if (data.role === 'admin') {
                        window.location.href = '/admin/dashboard';
                    } else if (data.role === 'librarian') {
                        window.location.href = '/librarian/dashboard';
                    } else if (data.role === 'member') {
                        window.location.href = '/member/dashboard';
                    } else {
                        alert('Unknown user role. Cannot redirect.');
                    }
                } else {
                    alert(data.message || 'Login failed. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error during login:', error);
                alert('An error occurred while trying to log in.');
            });
        });
    }

    // -----------------------------------------------------------------------------
    // Logout Handler
    // -----------------------------------------------------------------------------
    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            fetch('/auth/logout', { method: 'POST' })
                .then(response => {
                    // If logout is successful, remove any leftover tokens in localStorage (optional) 
                    localStorage.removeItem('access_token'); 
                    return response.json();
                })
                .then(() => {
                    // Redirect to login page
                    window.location.href = '/auth/login';
                })
                .catch(error => console.error('Error during logout:', error));
        });
    }
    // -----------------------------------------------------------------------------
// Fetch and Render Books (Enhanced for Dashboard)
// -----------------------------------------------------------------------------
// async function fetchBooks() {
//     try {
//         const response = await authFetch('/view_books');
//         const data = await response.json();
//         const booksTableBody = document.querySelector('#books-table tbody');
//         booksTableBody.innerHTML = data.books.map(book => `
//             <tr>
//                 <td>${book.book_id}</td>
//                 <td>${book.title}</td>
//                 <td>${book.author}</td>
//                 <td>${book.genre}</td>
//                 <td>${book.stock}</td>
//                 <td>
//                     <button onclick="editBook(${book.book_id})">Edit</button>
//                     <button onclick="deleteBook(${book.book_id})">Delete</button>
//                 </td>
//             </tr>
//         `).join('');
//     } catch (error) {
//         console.error('Error fetching books:', error);
//     }
// }

// async function editBook(id) {
//     try {
//         const book = await authFetch(`/update_book?id=${book_id}`);
//         document.getElementById('update-id').value = book.book_id;
//         document.getElementById('update-title').value = book.title;
//         document.getElementById('update-author').value = book.author;
//         document.getElementById('update-genre').value = book.genre;
//         document.getElementById('update-stock').value = book.stock;
//         document.getElementById('update-section').style.display = 'block';
//     } catch (error) {
//         console.error('Error fetching book for edit:', error);
//     }
// }

// document.getElementById('update-book-form').addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const id = document.getElementById('update-id').value;
//     const title = document.getElementById('update-title').value;
//     const author = document.getElementById('update-author').value;
//     const genre = document.getElementById('update-genre').value;
//     const stock = document.getElementById('update-stock').value;
//     try {
//         await authFetch(`/update_book/${id}`, {
//             method: 'PUT',
//             body: JSON.stringify({ title, author, genre, stock })
//         });
//         alert('Book updated successfully!');
//         document.getElementById('update-section').style.display = 'none';
//         fetchBooks();
//     } catch (error) {
//         console.error('Error updating book:', error);
//     }
// });

// async function deleteBook(id) {
//     if (confirm('Are you sure you want to delete this book?')) {
//         try {
//             await authFetch(`/delete_book/${book_id}`, { method: 'DELETE' });
//             alert('Book deleted successfully!');
//             fetchBooks();
//         } catch (error) {
//             console.error('Error deleting book:', error);
//         }
//     }
// }

// // Fetch books if we are on the librarian dashboard
// if (window.location.pathname === '/librarian/dashboard') {
//     fetchBooks();
// }

// // -----------------------------------------------------------------------------
// // Add Book Handler
// // -----------------------------------------------------------------------------
// document.getElementById('add-book-form').addEventListener('submit', async (e) => {
//     e.preventDefault();
//     const title = document.getElementById('add-title').value;
//     const author = document.getElementById('add-author').value;
//     const genre = document.getElementById('add-genre').value;
//     const stock = document.getElementById('add-stock').value;
//     try {
//         await authFetch('/add_book', {
//             method: 'POST',
//             body: JSON.stringify({ title, author, genre, stock })
//         });
//         alert('Book added successfully!');
//         document.getElementById('add-book-form').reset();
//         fetchBooks();
//     } catch (error) {
//         console.error('Error adding book:', error);
//     }
// });


});

