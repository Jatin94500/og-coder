# 📊 How to View Mermaid Diagrams

## The Error You're Seeing

If you see: `Error: MermaidError: No diagram type detected...`

This means your current viewer doesn't support Mermaid diagrams or has a rendering issue.

## ✅ Recommended Ways to View

### 1. GitHub (Best Option)
Simply push your code to GitHub and view the files there:
```bash
git add .
git commit -m "Add system diagrams"
git push
```
Then open `SYSTEM_DIAGRAMS.md` or `README.md` on GitHub - diagrams render automatically!

### 2. Mermaid Live Editor (Instant)
1. Go to: https://mermaid.live/
2. Copy any diagram code from `SYSTEM_DIAGRAMS.md`
3. Paste into the editor
4. See it render instantly
5. Export as PNG/SVG if needed

### 3. VS Code Extensions
Install one of these extensions:
- **Markdown Preview Mermaid Support** (recommended)
- **Mermaid Markdown Syntax Highlighting**
- **Markdown Preview Enhanced**

After installation:
1. Open `SYSTEM_DIAGRAMS.md` in VS Code
2. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac)
3. View rendered diagrams in preview pane

### 4. GitLab
GitLab also supports Mermaid natively - just view the markdown files there.

### 5. Online Markdown Editors
- **StackEdit**: https://stackedit.io/
- **Dillinger**: https://dillinger.io/
- **HackMD**: https://hackmd.io/

## 🔧 Troubleshooting

### Issue: Diagrams don't render in VS Code
**Solution**: 
1. Install "Markdown Preview Mermaid Support" extension
2. Reload VS Code
3. Open markdown file and use preview

### Issue: Syntax error in diagram
**Solution**: 
1. Copy the diagram code
2. Test in https://mermaid.live/
3. Fix any syntax issues there
4. Copy back to your file

### Issue: Viewer shows raw code
**Solution**: Your viewer doesn't support Mermaid. Use one of the recommended options above.

## 📱 Alternative: View as Images

If you need static images, use Mermaid Live Editor:

1. Go to https://mermaid.live/
2. Paste diagram code
3. Click "Actions" → "PNG" or "SVG"
4. Download the image
5. Add to your documentation

## 🎯 Quick Test

Try this simple diagram to test your viewer:

\`\`\`mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
\`\`\`

If you see a diagram with three boxes connected by arrows, your viewer works!

## 📚 Files with Diagrams

- `README.md` - Main architecture diagram
- `SYSTEM_DIAGRAMS.md` - 12 detailed diagrams
- `DIAGRAMS_SIMPLE.md` - Simplified versions

## 💡 Best Practice

For presentations or documentation that needs to work everywhere:
1. Render diagrams on Mermaid Live Editor
2. Export as PNG/SVG
3. Include images in your docs
4. Keep mermaid source in markdown for editing

## 🌐 Browser Support

Mermaid works in:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ GitHub/GitLab web interface
- ❌ Some older markdown viewers
- ❌ Basic text editors without plugins

## Example: Converting to Images

```bash
# Using mermaid-cli (if installed)
npm install -g @mermaid-js/mermaid-cli
mmdc -i SYSTEM_DIAGRAMS.md -o diagrams/
```

This creates PNG images of all diagrams in the `diagrams/` folder.

---

**Recommended**: Push to GitHub and view there - it's the easiest way! 🚀
