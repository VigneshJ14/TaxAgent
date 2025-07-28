# AI Tax Return Agent Prototype

A comprehensive end-to-end prototype for automating personal tax return preparation. This system allows users to upload standard tax documents (W-2, 1099-INT, 1099-NEC), extracts relevant data using advanced parsing techniques, calculates tax liability, and generates a completed IRS Form 1040.

## 🚀 Features

### Core Functionality
- **Multi-Document Upload**: Support for W-2, 1099-INT, and 1099-NEC forms
- **Advanced Document Processing**: Rule-based parsing with regex patterns for accurate data extraction
- **Real-Time Tax Calculation**: 2024 tax brackets with standard deductions and marginal tax calculation
- **Professional Form Generation**: Creates IRS Form 1040 that matches official blank forms
- **Precision Alignment**: Pixel-perfect text placement on generated forms

### User Experience
- **Drag-and-Drop Interface**: Easy file upload with visual feedback
- **Real-Time Validation**: File type, size, and duplicate content detection
- **Progress Tracking**: Step-by-step workflow with clear status indicators
- **Download Ready Forms**: Generated Form 1040 ready for submission

## 🛠 Technical Stack

### Frontend
- **React 18** with TypeScript
- **React Router DOM** for navigation
- **Axios** for API communication
- **Modern CSS** with responsive design

### Backend
- **Flask** with Blueprint architecture
- **Flask-CORS** for cross-origin requests
- **Python 3.8+** with virtual environment

### Document Processing
- **PyPDF2** for PDF manipulation and watermarking
- **PyMuPDF (fitz)** for advanced text analysis and coordinate detection
- **pdfplumber** for text extraction
- **ReportLab** for PDF generation
- **Rule-based parsing** with regex patterns for data extraction

### Tax Calculation
- **2024 Tax Brackets**: Single, Married, Head of Household
- **Standard Deductions**: Current IRS guidelines
- **Marginal Tax Calculation**: Accurate tax liability computation
- **AGI and Taxable Income**: Complete tax computation pipeline

## 📁 Project Structure

```
AI Tax Agent/
├── backend/                    # Flask API server
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   │   ├── main.py        # Health checks
│   │   │   ├── upload.py      # File upload handling
│   │   │   ├── process.py     # Document processing
│   │   │   ├── calculate.py   # Tax calculation
│   │   │   └── generate.py    # Form 1040 generation
│   │   └── services/          # Core business logic
│   │       ├── document_processor.py    # Document parsing
│   │       ├── tax_calculator.py       # Tax computation
│   │       ├── precision_form_filler.py # Primary form generator
│   │       └── robust_form_filler.py   # Backup form generator
│   ├── realistic_irs_forms/   # Sample tax documents
│   │   ├── filled-w2.pdf
│   │   ├── filled-1099int.pdf
│   │   ├── filled-1099nec.pdf
│   │   └── blank-1040.pdf
│   ├── requirements.txt       # Python dependencies
│   └── app.py                # Flask application entry
├── frontend/                  # React TypeScript application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service layer
│   │   └── types/            # TypeScript interfaces
│   ├── package.json          # Node.js dependencies
│   └── tsconfig.json         # TypeScript configuration
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 📋 API Endpoints

### File Upload
- `POST /api/upload` - Upload tax documents
- `GET /api/upload/status` - Check upload status
- `DELETE /api/upload/<filename>` - Delete specific file
- `DELETE /api/upload/clear` - Clear all uploads

### Document Processing
- `POST /api/process` - Process all uploaded documents
- `POST /api/process/<filename>` - Process specific document

### Tax Calculation
- `POST /api/calculate` - Full tax calculation
- `POST /api/calculate/estimate` - Quick tax estimate

### Form Generation
- `POST /api/generate-form-1040` - Generate Form 1040 (precision)
- `POST /api/generate-precision-form-1040` - Precision form filler
- `POST /api/generate-robust-form-1040` - Robust form filler

## 🔧 Development

### Testing the Complete Workflow
1. **Upload Documents**: Use the realistic IRS forms in `backend/realistic_irs_forms/`
2. **Process Documents**: Extract data from W-2, 1099-INT, and 1099-NEC
3. **Calculate Tax**: Verify tax calculations match expected values
4. **Generate Form**: Download completed Form 1040

### Debug Tools
- **Coordinate Analysis**: `backend/analyze_form_fields.py` - Analyze blank form coordinates
- **Debug Form Generation**: `backend/create_debug_form_with_units.py` - Generate forms with grid lines
- **Complete Verification**: `backend/test_complete_form_verification.py` - End-to-end testing


## 📊 Sample Data

The system includes realistic IRS forms for testing:
- `filled-w2.pdf` - Sample W-2 with wages and withholding
- `filled-1099int.pdf` - Sample 1099-INT with interest income
- `filled-1099nec.pdf` - Sample 1099-NEC with self-employment income
- `blank-1040.pdf` - Official IRS Form 1040 template

## 🔒 Security & Validation

- **File Type Validation**: Only PDF files accepted
- **Size Limits**: Configurable file size restrictions
- **Duplicate Detection**: SHA-256 content hashing
- **Input Validation**: Comprehensive form field validation
- **Error Handling**: Graceful error responses

## 🚀 Production Considerations

- **Environment Variables**: Configure for production deployment
- **Database Integration**: Replace file storage with database
- **Authentication**: Add user authentication and authorization
- **Logging**: Implement comprehensive logging
- **Testing**: Add unit and integration tests
- **Documentation**: API documentation with Swagger/OpenAPI

## 📝 License

This is a prototype project for educational and demonstration purposes.

---

**Status**: ✅ **Complete** - All phases implemented and tested
**Last Updated**: July 2024
**Version**: 1.0.0 
