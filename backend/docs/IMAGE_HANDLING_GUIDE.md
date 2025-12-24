# Handling Images in Questions - Complete Guide

## Current Setup ✅

Your Question model already has:
```python
diagram_url = models.URLField(blank=True, null=True, help_text="Optional diagram/image URL")
```

---

## 📸 Image Handling Options

### Option 1: **Upload to Backend** (Recommended) ✅
Store images in your backend's media folder.

**Pros:**
- Full control over images
- Fast loading
- No external dependencies
- Works offline

**Setup:**
```python
# models.py
class Question(models.Model):
    # Change from URLField to ImageField
    diagram = models.ImageField(
        upload_to='question_diagrams/', 
        blank=True, 
        null=True
    )
```

**File structure:**
```
backend/
├── media/
│   └── question_diagrams/
│       ├── q1_diagram.png
│       ├── q2_graph.jpg
│       └── q3_circuit.png
```

### Option 2: **Use External URLs** (Current Setup)
Store images on external services (Imgur, Cloudinary, etc.)

**Pros:**
- No storage on your server
- CDN delivery (fast)

**Cons:**
- Depends on external service
- URLs can break

### Option 3: **Base64 Encoding** (Not Recommended)
Embed images directly in database.

**Cons:**
- Large database size
- Slow queries

---

## 🎯 Recommended Approach

### Use Backend Media Storage

#### Step 1: Configure Django Media Settings

**File:** `backend/config/settings.py`

```python
# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### Step 2: Update URLs

**File:** `backend/config/urls.py`

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your existing urls
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### Step 3: Update Question Model

**File:** `backend/exams/models.py`

```python
class Question(models.Model):
    # ... existing fields ...
    
    # Option 1: Use ImageField (recommended)
    diagram = models.ImageField(
        upload_to='question_diagrams/%Y/%m/', 
        blank=True, 
        null=True,
        help_text="Optional diagram/image for the question"
    )
    
    # OR keep URLField for flexibility
    diagram_url = models.URLField(blank=True, null=True)
```

#### Step 4: Install Pillow

```bash
pip install Pillow
```

---

## 📝 CSV Format with Images

### Method 1: Upload Images First, Then Reference

**CSV Format:**
```csv
section_name,question_number,question_text,option_a,option_b,option_c,option_d,correct_option,marks,diagram_url
Engineering Mathematics,1,"Find the derivative...",Option A,Option B,Option C,Option D,A,1,/media/question_diagrams/2024/01/q1.png
```

**Workflow:**
1. Upload all images to `backend/media/question_diagrams/`
2. Reference them in CSV with relative paths
3. Import CSV

### Method 2: Upload Images via Admin Panel

1. Create question via CSV (without image)
2. Upload image via Django admin
3. Image automatically saved to media folder

---

## 🖼️ Frontend Display

### Update Exam Page to Show Images

**File:** `frontend/src/app/exam/[id]/page.tsx`

```tsx
<div className="mb-8">
  <h2 className="text-xl font-medium text-gray-800">
    {currentQuestionIndex + 1}. <MathText text={currentQuestion.text} />
  </h2>
  
  {/* Display diagram if exists */}
  {currentQuestion.diagram_url && (
    <div className="mt-4 p-4 bg-gray-50 rounded-lg">
      <img 
        src={`${process.env.NEXT_PUBLIC_API_URL?.replace('/api', '')}${currentQuestion.diagram_url}`}
        alt="Question diagram"
        className="max-w-full h-auto rounded-lg shadow-sm"
      />
    </div>
  )}
</div>
```

---

## 🔧 Image Upload Script

Create a helper script to upload images:

**File:** `backend/upload_question_images.py`

```python
import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Question
from django.core.files import File

def upload_image_for_question(question_id, image_path):
    """Upload image for a specific question"""
    question = Question.objects.get(id=question_id)
    
    with open(image_path, 'rb') as img_file:
        question.diagram.save(
            os.path.basename(image_path),
            File(img_file),
            save=True
        )
    
    print(f"✅ Image uploaded for Question {question_id}")

# Usage
upload_image_for_question(1, 'path/to/image.png')
```

---

## 📦 Bulk Image Upload

**File:** `backend/bulk_upload_images.py`

```python
import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exams.models import Question
from django.core.files import File

def bulk_upload_images(csv_file):
    """
    CSV format:
    question_id,image_path
    1,images/q1.png
    2,images/q2.jpg
    """
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_id = row['question_id']
            image_path = row['image_path']
            
            if os.path.exists(image_path):
                question = Question.objects.get(id=question_id)
                with open(image_path, 'rb') as img:
                    question.diagram.save(
                        os.path.basename(image_path),
                        File(img),
                        save=True
                    )
                print(f"✅ Uploaded image for Question {question_id}")
            else:
                print(f"❌ Image not found: {image_path}")

# Usage
bulk_upload_images('question_images.csv')
```

---

## 🎨 Image Best Practices

### 1. Image Format
- **PNG** - For diagrams, graphs (transparent background)
- **JPG** - For photos, complex images
- **SVG** - For simple diagrams (best quality, small size)

### 2. Image Size
- **Max width:** 800px (for mobile compatibility)
- **File size:** < 200KB per image
- **Compress** before uploading

### 3. Naming Convention
```
q{question_number}_{description}.png

Examples:
q1_circuit_diagram.png
q15_graph.jpg
q23_geometry.png
```

### 4. Folder Structure
```
media/
└── question_diagrams/
    ├── 2023/
    │   ├── engineering_math/
    │   ├── statistics/
    │   └── aptitude/
    ├── 2024/
    └── 2025/
```

---

## 🚀 Quick Start Workflow

### For Questions with Images:

1. **Prepare Images**
   ```bash
   mkdir -p backend/media/question_diagrams/2024
   # Copy all images to this folder
   ```

2. **Create CSV** (without images first)
   ```csv
   section_name,question_number,question_text,...
   ```

3. **Import Questions**
   ```bash
   python manage.py import_questions dcet_2024.csv
   ```

4. **Upload Images** (using script)
   ```bash
   python bulk_upload_images.py images_mapping.csv
   ```

5. **Verify** in admin panel

---

## 🔍 Testing Image Display

### Test Checklist:
- [ ] Image loads on exam page
- [ ] Image is responsive (mobile-friendly)
- [ ] Image doesn't break layout
- [ ] Image loads fast (< 1 second)
- [ ] Fallback if image fails to load

---

## 💡 My Recommendation

**Best approach for you:**

1. **Use ImageField** (not URLField) - Better control
2. **Upload images to backend/media** - No external dependencies
3. **Use bulk upload script** - Save time
4. **Compress images** - Faster loading

**Workflow:**
1. Create questions in CSV (no images)
2. Import CSV to database
3. Upload all images at once using script
4. Images automatically linked to questions

**Want me to:**
1. Update the Question model to use ImageField?
2. Create the bulk upload script?
3. Update frontend to display images?

Let me know and I'll implement it! 🚀
