# GitHub Pages Website Setup

This repository is configured to be published as a GitHub Pages website at:
**https://usdiseasetracker.github.io/USDiseaseTracker-Docs/**

## How It Works

The repository uses Jekyll with the "Documentation" theme from [jekyllthemes.io](https://jekyllthemes.io/theme/documentation) to automatically convert Markdown files into a professional documentation website. The site is built and deployed automatically whenever changes are pushed to the `main` branch.

All webpage-related files are organized in the `webpage/` directory.

### Key Components

1. **`webpage/_config.yml`** - Jekyll configuration file that controls:
   - Site title and description
   - Theme settings (using Documentation theme with Flatly Bootstrap theme)
   - Build settings
   - Collections and defaults

2. **`webpage/index.html`** - The landing page of the website with hero section

3. **`guides/`** - Documentation pages with Jekyll frontmatter:
   - `guides/data-submission-guide.md` - Data submission guide
   - `guides/data-technical-specs.md` - Technical specifications
   - `guides/data-transfer-guide.md` - Data transfer methods
   - `guides/validation.md` - Validation rules
   - `guides/pilot-overview.md` - Pilot program overview
   
   Note: Jekyll accesses these via symlink at `webpage/_guides/`

4. **`webpage/_data/docs.yml`** - Navigation structure for the documentation sidebar

5. **`webpage/_layouts/`** - Page layouts:
   - `default.html` - Base layout with navigation
   - `docs.html` - Documentation page layout with sidebar
   - `page.html` - Simple page layout
   - `post.html` - Blog post layout

6. **`webpage/_includes/`** - Reusable components:
   - `topnav.html` - Top navigation bar
   - `docs_nav.html` - Documentation sidebar navigation
   - `footer.html` - Site footer
   - `head.html` - HTML head with meta tags and CSS
   - Others

7. **`webpage/assets/`** - Static assets including:
   - CSS files (Bootstrap with Bootswatch themes)
   - JavaScript files
   - Images
   - Font Awesome icons

8. **`.github/workflows/deploy-pages.yml`** - GitHub Actions workflow that:
   - Builds the Jekyll site from the `webpage/` directory
   - Deploys it to GitHub Pages
   - Runs automatically on push to `main` branch

## Enabling GitHub Pages

To enable the website, a repository administrator needs to:

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment":
   - Source: Select **GitHub Actions**
3. The site will be available at `https://usdiseasetracker.github.io/USDiseaseTracker-Docs/`

## Making Changes

### Adding a New Documentation Page

1. Create a new Markdown file in `guides/` (e.g., `guides/my-new-page.md`)
2. Add front matter at the top:
   ```yaml
   ---
   title: My New Page
   permalink: /docs/my-new-page/
   ---
   ```
3. Add the page to navigation by editing `webpage/_data/docs.yml`:
   ```yaml
   - title: My Section
     docs:
     - my-new-page
   ```

### Updating Existing Pages

Simply edit the Markdown files in `guides/` and push to `main`:
- Changes to documentation pages update automatically
- The site rebuilds automatically (takes 1-2 minutes)

## Local Development

To preview the site locally:

```bash
# Install Ruby and Bundler (requires Ruby 2.5+)
gem install bundler

# Navigate to the webpage directory
cd webpage

# Install dependencies
bundle install

# Serve the site locally
bundle exec jekyll serve

# View at http://localhost:4000/USDiseaseTracker-Docs/
```

## Theme Customization

The site uses the Documentation theme with these customizations:

1. **Bootstrap theme**: Set in `webpage/_config.yml` with `bootwatch: flatly`
   - Available themes: cerulean, cosmo, cyborg, darkly, flatly, journal, lumen, paper, readable, sandstone, simplex, slate, solar, spacelab, superhero, united, yeti

2. **Custom CSS**: Modify `webpage/_sass/_jekyll-doc-theme.scss` for custom styles

3. **Logo**: Replace `webpage/assets/img/logonav.png` with your own logo

4. **Favicon**: Replace `webpage/favicon.ico`

## Troubleshooting

- **Site not updating?** Check the Actions tab for build status
- **Links broken?** Ensure relative links use `{{ "/path/" | relative_url }}` in Liquid templates
- **Sidebar not showing?** Check that pages are listed in `webpage/_data/docs.yml`
- **404 errors?** Verify the permalink in the page's front matter

For more information, see:
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Documentation Theme](https://aksakalli.github.io/jekyll-doc-theme/)

