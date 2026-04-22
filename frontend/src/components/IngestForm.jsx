import React, { useState, useRef } from 'react';
import { UploadCloud, CheckCircle, Database } from 'lucide-react';
import './IngestForm.css';

const IngestForm = () => {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, loading, success, error
    const [message, setMessage] = useState('');
    const fileInputRef = useRef(null);

    const handleFileSubmit = async (e) => {
        e.preventDefault();
        if (!file) return;

        setStatus('loading');
        setMessage('');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('http://localhost:8000/upload-dataset', {
                method: 'POST',
                body: formData
            });

            if (!res.ok) {
                const errData = await res.json();
                throw new Error(errData.error || 'Failed to upload dataset');
            }

            const data = await res.json();
            setStatus('success');
            setMessage(data.message);
            setFile(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }

            setTimeout(() => {
                setStatus('idle');
                setMessage('');
            }, 5000);

        } catch (err) {
            setStatus('error');
            setMessage(err.message || 'An error occurred');
            
            setTimeout(() => {
                setStatus('idle');
                setMessage('');
            }, 5000);
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setFile(e.target.files[0]);
        }
    };

    return (
        <div className="ingest-card">
            <div className="ingest-header">
                <Database className="icon-main" />
                <h2>Knowledge Base</h2>
                <p>Upload .txt or .json datasets to train your Chatbot.</p>
            </div>
            
            <form onSubmit={handleFileSubmit}>
                <div className="file-upload-container" onClick={() => fileInputRef.current.click()}>
                    <div className="file-upload-box">
                        <UploadCloud size={40} className="file-icon" />
                        {file ? (
                            <p className="file-name">{file.name}</p>
                        ) : (
                            <p className="file-placeholder">Click to select a .txt or .json dataset file</p>
                        )}
                    </div>
                    <input 
                        type="file" 
                        accept=".txt,.csv,.md,.json" 
                        ref={fileInputRef}
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                        disabled={status === 'loading'}
                    />
                </div>

                <div className="status-container">
                    {status === 'success' && <p className="success-msg"><CheckCircle size={16}/> {message}</p>}
                    {status === 'error' && <p className="error-msg">{message}</p>}
                </div>

                <button 
                    type="submit" 
                    className={`submit-btn ${status === 'loading' ? 'loading' : ''}`}
                    disabled={status === 'loading' || !file}
                >
                    {status === 'loading' ? (
                        <div className="spinner"></div>
                    ) : (
                        <><UploadCloud size={18} /> Process Dataset</>
                    )}
                </button>
            </form>
        </div>
    );
};

export default IngestForm;
