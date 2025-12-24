# Font Analysis & Recommendations for DCET Exams

## Current Setup

### Fonts in Use
- **Body Text**: Inter (Google Font)
- **Headings**: Outfit (Google Font)
- **Math/LaTeX**: KaTeX default fonts

### Issue Identified
**DCET 2023** and **DCET 2025** use different LaTeX formatting:
- **2023**: `\textbf{text}` - Plain LaTeX commands
- **2025**: `$\text{text}$` - Math mode with dollar signs

This causes **different rendering** even though both use KaTeX.

## Best Fonts for Exams

### Recommended: Keep Current Setup ✅

**Why Inter + Outfit works well for exams:**

1. **Inter (Body)**
   - ✅ Excellent readability at all sizes
   - ✅ Clear distinction between similar characters (1, l, I)
   - ✅ Optimized for screen reading
   - ✅ Professional and clean
   - ✅ Wide language support

2. **Outfit (Headings)**
   - ✅ Modern and approachable
   - ✅ Good contrast with Inter
   - ✅ Clear hierarchy

3. **KaTeX (Math)**
   - ✅ Industry standard for math rendering
   - ✅ Matches LaTeX output
   - ✅ Familiar to students

### Alternative Recommendations

If you want to change fonts, here are the best options for exams:

#### Option 1: IBM Plex Sans (Professional)
```javascript
import { IBM_Plex_Sans } from 'next/font/google';
```
- Very readable
- Used by many educational platforms
- Excellent for long reading sessions

#### Option 2: Open Sans (Classic)
```javascript
import { Open_Sans } from 'next/font/google';
```
- Time-tested for readability
- Used by Google, WordPress
- Safe choice for all ages

#### Option 3: Roboto (Modern)
```javascript
import { Roboto } from 'next/font/google';
```
- Material Design standard
- Very familiar to users
- Clean and modern

## Standardization Recommendation

### Fix the LaTeX Inconsistency

**Problem**: Mixed LaTeX formats between 2023 and 2025
**Solution**: Standardize to one format

**Recommended Format**: Use `$...$` for inline math (2025 style)

**Why?**
- ✅ More explicit (clear start/end)
- ✅ Better KaTeX parsing
- ✅ Standard in markdown/Jupyter notebooks
- ✅ Easier to identify math vs text

### Action Items

1. **Keep current fonts** (Inter + Outfit) - they're excellent for exams
2. **Standardize LaTeX format** - convert 2023 to use `$...$` like 2025
3. **Optional**: Increase font size slightly for better readability
   - Body: 16px → 17px
   - Questions: 17px → 18px

## Font Size Recommendations for Exams

```css
/* Optimal sizes for exam readability */
body: 16-17px
questions: 17-18px
options: 16-17px
headings: 24-32px
```

## Conclusion

**Current fonts are great!** Inter and Outfit are excellent choices for an exam platform.

**Main issue**: LaTeX format inconsistency, not the fonts themselves.

**Recommendation**: Keep fonts, standardize LaTeX formatting.
