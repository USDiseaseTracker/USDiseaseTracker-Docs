# GitHub Pages Website Setup

This repository is configured to be published as a GitHub Pages website at:
**https://usdiseasetracker.github.io/USDiseaseTracker-Docs/**

## How It Works

The repository uses Jekyll to automatically convert Markdown files into a website. The site is built and deployed automatically whenever changes are pushed to the `main` branch.

### Key Components

1. **`_config.yml`** - Jekyll configuration file that controls:
   - Site title and description
   - Theme (currently using `jekyll-theme-cayman`)
   - Build settings
   - Which files to include/exclude

2. **`index.md`** - The landing page of the website

3. **`.github/workflows/deploy-pages.yml`** - GitHub Actions workflow that:
   - Builds the Jekyll site
   - Deploys it to GitHub Pages
   - Runs automatically on push to `main` branch

4. **Markdown Files** - All `.md` files in the repository are automatically converted to HTML pages:
   - `guides/*.md` → Available at `/guides/filename/`
   - `README.md` → Available at `/README/`
   - etc.

## Enabling GitHub Pages

To enable the website, a repository administrator needs to:

1. Go to repository **Settings** → **Pages**
2. Under "Build and deployment":
   - Source: Select **GitHub Actions**
3. The site will be available at `https://usdiseasetracker.github.io/USDiseaseTracker-Docs/`

## Making Changes

Simply edit the Markdown files and push to `main`:
- Changes to `index.md` update the homepage
- Changes to files in `guides/` update those documentation pages
- The site rebuilds automatically (takes 1-2 minutes)

## Local Development

To preview the site locally:

```bash
# Install Jekyll (requires Ruby)
gem install bundler jekyll

# Create a Gemfile (one-time setup)
echo "source 'https://rubygems.org'" > Gemfile
echo "gem 'github-pages', group: :jekyll_plugins" >> Gemfile

# Install dependencies
bundle install

# Serve the site locally
bundle exec jekyll serve

# View at http://localhost:4000/USDiseaseTracker-Docs/
```

## Theme Customization

The site currently uses the Cayman theme. To customize:

1. **Change theme**: Edit `theme:` in `_config.yml`
   - Available themes: https://pages.github.com/themes/

2. **Custom CSS**: Create `assets/css/style.scss`:
   ```scss
   ---
   ---
   @import "{{ site.theme }}";
   
   /* Your custom CSS here */
   ```

3. **Custom layouts**: Create `_layouts/default.html` to override theme layout

## Troubleshooting

- **Site not updating?** Check the Actions tab for build status
- **Links broken?** Ensure relative links use correct paths
- **404 errors?** Check that files are included in `_config.yml`

For more information, see:
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
