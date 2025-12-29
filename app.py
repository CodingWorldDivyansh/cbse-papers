"""
CBSE Previous Year Papers - Flask Backend
Direct PDF downloads with multiple mirror fallback
Supports: Question Papers, Marking Schemes, Sample Papers, Compartment Papers
Years: 2015-2025 | Subjects: Math, Accountancy, Economics, Business Studies, English, Data Science
"""

import io
import zipfile
import concurrent.futures
from flask import Flask, render_template, jsonify, request, Response, send_file
from flask_cors import CORS
import requests
from paper_database_v3 import (
    get_all_papers, get_paper_by_id, filter_papers,
    get_filter_options, SUBJECTS, YEARS, PAPER_TYPES, get_paper_count, get_stats
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Different headers for different mirrors
HEADERS_SUPERCOP = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,*/*',
    'Referer': 'https://supercop.in/',
}

HEADERS_SELFSTUDY = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,*/*',
    'Referer': 'https://www.selfstudys.com/',
}

HEADERS_CBSE = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,*/*',
    'Referer': 'https://cbse.gov.in/',
}

HEADERS_AGLASEM = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,*/*',
    'Referer': 'https://schools.aglasem.com/',
}

HEADERS_EXAMFEAR = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/pdf,*/*',
    'Referer': 'https://www.examfear.com/',
}

# Cache for successful URLs
url_cache = {}


def get_headers_for_mirror(mirror_name):
    """Get appropriate headers for each mirror"""
    if 'supercop' in mirror_name:
        return HEADERS_SUPERCOP
    elif 'selfstudy' in mirror_name:
        return HEADERS_SELFSTUDY
    elif 'aglasem' in mirror_name:
        return HEADERS_AGLASEM
    elif 'examfear' in mirror_name:
        return HEADERS_EXAMFEAR
    else:
        return HEADERS_CBSE


def fetch_pdf_from_url(url, headers, timeout=15):
    """Try to fetch PDF from a single URL"""
    try:
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            content = response.content
            # Verify it's actually a PDF
            if content[:4] == b'%PDF' or 'pdf' in response.headers.get('Content-Type', '').lower():
                return content
    except requests.RequestException:
        pass
    return None


def fetch_pdf(paper):
    """Fetch PDF with multiple mirror fallback - tries all URLs until one works"""
    urls = paper.get('urls', [])
    paper_id = paper.get('id')
    
    # Check cache first
    if paper_id in url_cache:
        cached_url, cached_mirror = url_cache[paper_id]
        headers = get_headers_for_mirror(cached_mirror)
        content = fetch_pdf_from_url(cached_url, headers)
        if content:
            return content, paper['filename']
    
    # Try each mirror URL
    for mirror_name, url in urls:
        headers = get_headers_for_mirror(mirror_name)
        content = fetch_pdf_from_url(url, headers)
        if content:
            # Cache successful URL
            url_cache[paper_id] = (url, mirror_name)
            return content, paper['filename']
    
    return None, None


def fetch_pdf_batch(papers, max_workers=5):
    """Fetch multiple PDFs concurrently"""
    results = {}
    
    def fetch_single(paper):
        content, filename = fetch_pdf(paper)
        return paper['id'], content, filename or paper['filename']
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_single, p): p['id'] for p in papers}
        for future in concurrent.futures.as_completed(futures):
            paper_id, content, filename = future.result()
            results[paper_id] = (content, filename)
    
    return results


PLACEHOLDER_PDF = b'''%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj
4 0 obj<</Length 150>>stream
BT
/F1 16 Tf
50 700 Td
(CBSE Paper - Temporarily Unavailable) Tj
0 -30 Td
/F1 12 Tf
(Please try again later or check CBSE official website) Tj
ET
endstream endobj
5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000052 00000 n 
0000000105 00000 n 
0000000246 00000 n 
0000000446 00000 n 
trailer<</Size 6/Root 1 0 R>>
startxref
515
%%EOF'''


@app.route('/')
def index():
    import os
    import base64
    # Try templates folder first, fall back to embedded HTML
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
    if os.path.exists(template_path):
        return render_template('index.html')
    # Embedded HTML (base64 encoded to avoid escaping issues)
    embedded_html_b64 = open(os.path.join(os.path.dirname(__file__), 'index_html.b64'), 'r').read()
    return base64.b64decode(embedded_html_b64).decode('utf-8')

@app.route('/download-source')
def download_source():
    """Download the source code ZIP for deployment"""
    import os
    zip_path = os.path.join(os.path.dirname(__file__), 'cbse-papers-deploy.zip')
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True, download_name='cbse-papers-deploy.zip')
    return "ZIP file not found", 404


@app.route('/api/papers')
def api_papers():
    year = request.args.get('year')
    subject = request.args.get('subject')
    paper_type = request.args.get('type')
    region = request.args.get('region')
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    papers = filter_papers(year=year, subject=subject, paper_type=paper_type,
                          region=region, search=search)
    
    total = len(papers)
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_papers = papers[start:end]
    
    # Remove urls from response to reduce payload (they're internal)
    clean_papers = []
    for p in paginated_papers:
        clean_p = {k: v for k, v in p.items() if k != 'urls'}
        clean_papers.append(clean_p)

    return jsonify({
        'papers': clean_papers,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page,
        'filters': get_filter_options()
    })


@app.route('/api/filters')
def api_filters():
    return jsonify(get_filter_options())


@app.route('/api/stats')
def api_stats():
    """Get database statistics"""
    stats = get_stats()
    return jsonify({
        'total_papers': stats['total'],
        'by_subject': stats['by_subject'],
        'by_year': stats['by_year'],
        'by_type': stats['by_type'],
        'subjects': SUBJECTS,
        'years': YEARS,
        'types': PAPER_TYPES
    })


@app.route('/api/download/<int:paper_id>')
def download_paper(paper_id):
    """Download single paper - DIRECT without redirection, with mirror fallback"""
    paper = get_paper_by_id(paper_id)

    if not paper:
        return jsonify({'error': 'Paper not found'}), 404

    pdf_content, filename = fetch_pdf(paper)

    if pdf_content:
        return Response(
            pdf_content,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'application/pdf',
                'Cache-Control': 'no-cache',
                'X-Download-Status': 'success'
            }
        )

    # Return placeholder if all mirrors fail
    return Response(
        PLACEHOLDER_PDF,
        mimetype='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename="{paper["filename"]}"',
            'Content-Type': 'application/pdf',
            'X-Download-Status': 'placeholder'
        }
    )


@app.route('/api/download-zip', methods=['POST'])
def download_zip():
    """Download multiple papers as ZIP - DIRECT without redirection"""
    data = request.get_json()
    paper_ids = data.get('paper_ids', [])

    if not paper_ids:
        return jsonify({'error': 'No papers selected'}), 400

    if len(paper_ids) > 100:
        return jsonify({'error': 'Maximum 100 papers per download'}), 400

    # Get all papers
    papers = [get_paper_by_id(pid) for pid in paper_ids]
    papers = [p for p in papers if p is not None]

    if not papers:
        return jsonify({'error': 'No valid papers found'}), 404

    # Fetch PDFs concurrently
    results = fetch_pdf_batch(papers, max_workers=10)

    zip_buffer = io.BytesIO()
    success_count = 0
    fail_count = 0

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for paper in papers:
            paper_id = paper['id']
            content, filename = results.get(paper_id, (None, paper['filename']))

            if content:
                zip_file.writestr(filename, content)
                success_count += 1
            else:
                # Add placeholder for failed downloads
                zip_file.writestr(f"UNAVAILABLE_{filename}", PLACEHOLDER_PDF)
                fail_count += 1

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='CBSE_Papers.zip'
    )


@app.route('/api/download-filtered', methods=['POST'])
def download_filtered():
    """Download all papers matching current filters as ZIP"""
    data = request.get_json()
    
    year = data.get('year')
    subject = data.get('subject')
    paper_type = data.get('type')
    region = data.get('region')
    
    papers = filter_papers(year=year, subject=subject, paper_type=paper_type, region=region)
    
    if not papers:
        return jsonify({'error': 'No papers match the filters'}), 404
    
    if len(papers) > 100:
        return jsonify({'error': f'Too many papers ({len(papers)}). Please narrow your filters. Max 100.'}), 400
    
    # Fetch PDFs concurrently
    results = fetch_pdf_batch(papers, max_workers=10)
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for paper in papers:
            paper_id = paper['id']
            content, filename = results.get(paper_id, (None, paper['filename']))
            
            if content:
                zip_file.writestr(filename, content)
            else:
                zip_file.writestr(f"UNAVAILABLE_{filename}", PLACEHOLDER_PDF)
    
    zip_buffer.seek(0)
    
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='CBSE_Papers_Filtered.zip'
    )


@app.route('/api/check/<int:paper_id>')
def check_paper(paper_id):
    """Check if paper is available from any mirror"""
    paper = get_paper_by_id(paper_id)
    if not paper:
        return jsonify({'error': 'Not found'}), 404

    urls = paper.get('urls', [])
    results = []
    
    for mirror_name, url in urls:
        headers = get_headers_for_mirror(mirror_name)
        try:
            response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            results.append({
                'mirror': mirror_name,
                'url': url,
                'status': response.status_code,
                'available': response.status_code == 200
            })
        except Exception as e:
            results.append({
                'mirror': mirror_name,
                'url': url,
                'status': 0,
                'available': False,
                'error': str(e)
            })
    
    available = any(r['available'] for r in results)
    
    return jsonify({
        'id': paper_id,
        'display_name': paper['display_name'],
        'available': available,
        'mirrors': results
    })


if __name__ == '__main__':
    print(f"Starting CBSE Papers Server with {get_paper_count()} papers in database")
    app.run(host='0.0.0.0', port=12000, debug=True)

