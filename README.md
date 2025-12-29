# 📚 CBSE Previous Year Papers Portal

A comprehensive web portal to download CBSE Class 12 previous year papers (2015-2025) with **direct PDF downloads** from multiple mirror sites.

## ✨ Features

### 📊 Massive Paper Database
- **1,819+ papers** across 6 subjects and 11 years (2015-2025)
- **Multiple paper types**: Question Papers, Marking Schemes, Sample Papers, Compartment Papers
- **All regions covered**: Delhi, Outside Delhi, All India, Foreign Sets
- **All paper sets**: Set 1, Set 2, Set 3 for each region

### 📖 Subjects Covered
1. **Mathematics** - 345 papers
2. **Accountancy** - 345 papers  
3. **Economics** - 345 papers
4. **Business Studies** - 344 papers
5. **English Core** - 310 papers
6. **Data Science** - 130 papers

### 🌐 Multiple Mirror Fallbacks
Papers are fetched from multiple verified sources with automatic fallback:
- **Supercop.in** - Primary source for most subjects
- **Vedantu** - Secondary fallback
- **SelfStudy** - Tertiary fallback (includes Data Science)
- **Aglasem** - Additional mirror
- **CBSE Academic** - Official sample papers
- **ExamFear** - Additional backup

### 🚀 Key Capabilities
- ✅ **Direct PDF downloads** (no redirects)
- ✅ **Bulk download as ZIP** (select multiple papers)
- ✅ **Filter by year, subject, type, region**
- ✅ **Search functionality**
- ✅ **Select all filtered papers** for download
- ✅ **Automatic mirror fallback** if primary source fails
- ✅ **Responsive design** for mobile and desktop
- ✅ **Fast concurrent downloads** for ZIP creation

## 📈 Statistics

| Metric | Count |
|--------|-------|
| **Total Papers** | 1,819 |
| **Question Papers** | 870 |
| **Marking Schemes** | 870 |
| **Sample Papers** | 60 |
| **Compartment Papers** | 19 |
| **Years Covered** | 11 (2015-2025) |
| **Subjects** | 6 |
| **Mirror Sites** | 6+ |

### Papers by Year
- 2015: 150 papers
- 2016: 150 papers
- 2017: 150 papers
- 2018: 150 papers
- 2019: 154 papers
- 2020: 153 papers
- 2021: 192 papers (including all available papers)
- 2022: 196 papers
- 2023: 196 papers
- 2024: 196 papers
- 2025: 132 papers (latest available)

## 🛠️ Technical Stack

### Backend
- **Python 3.x** with Flask
- **Flask-CORS** for cross-origin requests
- **Requests** library for HTTP operations
- **Concurrent downloads** using ThreadPoolExecutor
- **Gunicorn** for production deployment

### Frontend
- Pure HTML/CSS/JavaScript
- Responsive design with modern UI
- Real-time filtering and search
- Toast notifications for user feedback

### Database
- **paper_database_v3.py**: Enhanced paper database with 1,819 entries
- In-memory data structure for blazing-fast queries
- Comprehensive URL mapping for multiple mirrors
- Smart fallback logic for failed downloads

## 📥 Installation & Setup

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd webapp

# Install dependencies
pip install -r requirements.txt

# Run the development server
python3 app.py
```

The application will start on `http://localhost:12000`

### Production Deployment

#### Using Gunicorn
```bash
gunicorn app:app --bind 0.0.0.0:12000 --workers 4
```

#### Using Render.com
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Use provided `render.yaml` configuration
5. Deploy automatically

## 📂 Project Structure

```
webapp/
├── app.py                    # Flask backend with API endpoints
├── paper_database_v3.py      # Enhanced paper database (1,819 papers)
├── index.html                # Frontend HTML/CSS/JS
├── requirements.txt          # Python dependencies
├── Procfile                  # Process file for deployment
├── render.yaml              # Render.com configuration
├── runtime.txt              # Python version specification
└── README.md                # This file
```

## 🔌 API Endpoints

### GET `/api/papers`
Fetch papers with optional filters
- **Query params**: `year`, `subject`, `type`, `region`, `search`, `page`, `per_page`
- **Returns**: Paginated list of papers with metadata

### GET `/api/stats`
Get database statistics
- **Returns**: Total counts by subject, year, and type

### GET `/api/filters`
Get available filter options
- **Returns**: Lists of years, subjects, types, and regions

### GET `/api/download/<paper_id>`
Download single paper as PDF
- **Returns**: Direct PDF file with proper headers

### POST `/api/download-zip`
Download multiple papers as ZIP
- **Body**: `{"paper_ids": [1, 2, 3]}`
- **Returns**: ZIP file containing selected papers

### POST `/api/download-filtered`
Download all papers matching current filters
- **Body**: Filter parameters
- **Returns**: ZIP file with filtered papers

### GET `/api/check/<paper_id>`
Check paper availability across mirrors
- **Returns**: Status of each mirror source

## 🎯 Key Improvements (v3 Database)

### From 886 → 1,819 Papers (+105% increase)

1. **Added Data Science subject** (130 papers) - Previously missing entirely
2. **Enhanced English Core coverage** (310 papers) - Added SelfStudy mirror
3. **Added 2021 papers** across all subjects (192 papers)
4. **Compartment papers** (19 papers) - New paper type added
5. **Multiple mirror URLs** for each paper - Better download success rate
6. **SelfStudy integration** - Additional verified source
7. **Aglasem integration** - Extra fallback option
8. **Sample papers for 2021-22** - Previously missing

### Enhanced Mirror Strategy
- **Primary**: Supercop (verified working URLs)
- **Secondary**: Vedantu (question papers only)
- **Tertiary**: SelfStudy (both QP and MS, includes Data Science)
- **Quaternary**: Aglasem (additional backup)
- **Official**: CBSE Academic (sample papers)

### Smart Fallback Logic
When downloading a paper, the system:
1. Checks cache for previously successful URL
2. Tries primary mirror (Supercop)
3. Falls back to secondary (Vedantu)
4. Falls back to tertiary (SelfStudy)
5. Falls back to quaternary (Aglasem)
6. Returns placeholder PDF if all fail (with error message)

## 🚀 Performance Features

- **Concurrent downloads**: Up to 10 parallel downloads for ZIP creation
- **URL caching**: Remembers working URLs to skip failed mirrors
- **Pagination**: 50 papers per page for smooth UI
- **Lazy loading**: Papers loaded on-demand
- **Compressed ZIP**: Efficient ZIP_DEFLATED compression

## 🎨 UI Features

- Modern gradient design
- Responsive layout (mobile-friendly)
- Real-time filter updates
- Toast notifications
- Loading indicators
- Error handling with fallbacks
- Checkbox selection for bulk downloads
- "Select All" functionality
- Download status tracking

## 🔒 Error Handling

- Graceful degradation if mirrors fail
- Placeholder PDF for unavailable papers
- Toast notifications for user feedback
- Console logging for debugging
- Timeout protection (15s per download)
- Maximum 100 papers per ZIP (to prevent server overload)

## 📝 Future Enhancements

- [ ] Add progress bar for ZIP downloads
- [ ] Implement paper preview feature
- [ ] Add download history
- [ ] Enable dark mode
- [ ] Add paper quality ratings
- [ ] Implement user accounts
- [ ] Add favorite papers feature
- [ ] Enable direct sharing links

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is for educational purposes. All papers are property of CBSE.

## 🙏 Credits

- **CBSE** for original papers
- **Supercop.in** for hosting papers
- **Vedantu** for mirror hosting
- **SelfStudy** for additional papers
- **Aglasem** for backup hosting
- **ExamFear** for additional resources

## 📞 Support

For issues or questions:
1. Check existing issues
2. Create a new issue with details
3. Provide error logs if applicable

---

**Made with ❤️ for CBSE students**

*Last updated: December 2024*
*Database version: v3*
*Total papers: 1,819*
