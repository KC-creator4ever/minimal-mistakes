# Instructions to Create Forest Skin Branch

Since the `forest-skin` branch was created locally but cannot be automatically pushed, here are the steps to recreate it:

## Option 1: Create from this branch

```bash
# Make sure you're on the copilot/add-beach-skin branch
git checkout copilot/add-beach-skin

# Create the forest-skin branch
git checkout -b forest-skin

# Edit _config.yml and change the skin from "beach" to "forest"
# Line 15: minimal_mistakes_skin: "forest"

# Commit the change
git add _config.yml
git commit -m "Update config to use forest skin"

# Push to GitHub
git push -u origin forest-skin
```

## Option 2: Apply the patch

```bash
# From the copilot/add-beach-skin branch
git checkout -b forest-skin

# Apply this change to _config.yml:
# Change line 15 from:
#   minimal_mistakes_skin    : "beach"
# To:
#   minimal_mistakes_skin    : "forest"

git add _config.yml
git commit -m "Update config to use forest skin"
git push -u origin forest-skin
```

## Verify

After creating the branch, build and serve the site to verify:

```bash
bundle exec jekyll build
bundle exec jekyll serve
```

Visit http://localhost:4000 to see the forest theme in action!
