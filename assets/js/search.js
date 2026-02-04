(function() {
  'use strict';

  // Search data will be loaded from search-data.json
  let searchData = [];
  let searchInput;
  let searchResults;

  // Initialize search when DOM is ready
  function init() {
    searchInput = document.getElementById('search-input');
    searchResults = document.getElementById('search-results');

    if (!searchInput || !searchResults) {
      console.warn('Search elements not found');
      return;
    }

    // Load search data
    loadSearchData();

    // Add event listeners
    searchInput.addEventListener('input', handleSearch);
    
    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.classList.remove('active');
      }
    });
  }

  // Load search data from JSON file
  function loadSearchData() {
    // Get baseurl from the page's base tag or use default
    const baseTag = document.querySelector('base');
    const baseUrl = baseTag ? baseTag.href : window.location.origin + '/USDiseaseTracker-Docs';
    
    fetch(baseUrl + '/search-data.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to load search data');
        }
        return response.json();
      })
      .then(data => {
        searchData = data;
      })
      .catch(error => {
        console.error('Error loading search data:', error);
        // Create fallback search data from current page
        createFallbackSearchData();
      });
  }

  // Create fallback search data from pages in the current site
  function createFallbackSearchData() {
    searchData = [
      {
        title: 'Home',
        url: '/USDiseaseTracker-Docs/',
        content: 'US Disease Tracker Documentation data standards templates examples validation'
      }
    ];
  }

  // Handle search input
  function handleSearch(e) {
    const query = e.target.value.trim().toLowerCase();

    if (query.length === 0) {
      searchResults.classList.remove('active');
      searchResults.innerHTML = '';
      return;
    }

    if (query.length < 2) {
      return; // Wait for at least 2 characters
    }

    const results = performSearch(query);
    displayResults(results, query);
  }

  // Perform search on the data
  function performSearch(query) {
    const queryTerms = query.split(/\s+/).filter(term => term.length > 0);
    
    return searchData
      .map(item => {
        let score = 0;
        const titleLower = item.title.toLowerCase();
        const contentLower = item.content.toLowerCase();

        queryTerms.forEach(term => {
          // Title matches are worth more
          if (titleLower.includes(term)) {
            score += 10;
          }
          // Content matches
          if (contentLower.includes(term)) {
            score += 1;
          }
        });

        return { ...item, score };
      })
      .filter(item => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 10); // Limit to top 10 results
  }

  // Display search results
  function displayResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = '<div class="no-results">No results found</div>';
      searchResults.classList.add('active');
      return;
    }

    // Clear previous results
    searchResults.innerHTML = '';
    
    results.forEach(result => {
      const highlightedTitle = highlightText(result.title, query);
      const excerpt = createExcerpt(result.content, query);
      
      const resultItem = document.createElement('div');
      resultItem.className = 'search-result-item';
      resultItem.innerHTML = `
        <div class="search-result-title">${highlightedTitle}</div>
        <div class="search-result-excerpt">${excerpt}</div>
      `;
      
      // Add click handler to navigate to result
      resultItem.addEventListener('click', function() {
        window.location.href = result.url;
      });
      
      searchResults.appendChild(resultItem);
    });

    searchResults.classList.add('active');
  }

  // Highlight query terms in text
  function highlightText(text, query) {
    const terms = query.split(/\s+/).filter(term => term.length > 0);
    let result = text;

    terms.forEach(term => {
      const regex = new RegExp(`(${escapeRegex(term)})`, 'gi');
      result = result.replace(regex, '<span class="search-highlight">$1</span>');
    });

    return result;
  }

  // Create excerpt with highlighted terms
  function createExcerpt(content, query, maxLength = 150) {
    const terms = query.split(/\s+/).filter(term => term.length > 0);
    const contentLower = content.toLowerCase();
    
    // Find first occurrence of any query term
    let firstIndex = -1;
    terms.forEach(term => {
      const index = contentLower.indexOf(term.toLowerCase());
      if (index !== -1 && (firstIndex === -1 || index < firstIndex)) {
        firstIndex = index;
      }
    });

    let excerpt;
    if (firstIndex !== -1) {
      // Show context around the match
      const start = Math.max(0, firstIndex - 50);
      const end = Math.min(content.length, firstIndex + maxLength);
      excerpt = (start > 0 ? '...' : '') + content.substring(start, end) + (end < content.length ? '...' : '');
    } else {
      // Just show beginning
      excerpt = content.substring(0, maxLength) + (content.length > maxLength ? '...' : '');
    }

    return highlightText(excerpt, query);
  }

  // Escape special regex characters
  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
