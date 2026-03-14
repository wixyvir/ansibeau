import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, Loader2 } from 'lucide-react';
import { submitLog } from '../services/api';

type InputMode = 'paste' | 'file';

function SubmitPage() {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [fileName, setFileName] = useState<string | null>(null);
  const [inputMode, setInputMode] = useState<InputMode>('paste');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    document.title = 'Submit Log - Ansibeau';
    return () => { document.title = 'Ansibeau'; };
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (ev) => {
      setContent(ev.target?.result as string);
    };
    reader.onerror = () => {
      setError('Failed to read file');
    };
    reader.readAsText(file);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      const log = await submitLog(title || 'Untitled Log', content);
      navigate(`/log/${log.id}`);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(message);
      setSubmitting(false);
    }
  };

  const canSubmit = content.trim().length > 0 && !submitting;

  return (
    <div className="min-h-screen bg-slate-900 py-6 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-slate-100 mb-6">Submit Ansible Log</h1>

        <form onSubmit={handleSubmit} className="bg-slate-800 border border-slate-700 rounded-lg p-6 shadow-lg">
          {/* Title */}
          <div className="mb-4">
            <label htmlFor="title" className="block text-sm font-medium text-slate-300 mb-1">
              Title
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Production Deploy 2024-01-15"
              disabled={submitting}
              className="w-full bg-slate-700 border border-slate-600 rounded-md px-3 py-2 text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50"
            />
          </div>

          {/* Input mode toggle */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-slate-300 mb-1">
              Log Content
            </label>
            <div className="flex gap-1 mb-3">
              <button
                type="button"
                onClick={() => setInputMode('paste')}
                disabled={submitting}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                  inputMode === 'paste'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                } disabled:opacity-50`}
              >
                <FileText className="inline-block w-4 h-4 mr-1 -mt-0.5" />
                Paste
              </button>
              <button
                type="button"
                onClick={() => setInputMode('file')}
                disabled={submitting}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                  inputMode === 'file'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                } disabled:opacity-50`}
              >
                <Upload className="inline-block w-4 h-4 mr-1 -mt-0.5" />
                File
              </button>
            </div>

            {/* Paste textarea */}
            {inputMode === 'paste' && (
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste your Ansible log output here..."
                disabled={submitting}
                rows={16}
                className="w-full bg-slate-700 border border-slate-600 rounded-md px-3 py-2 text-slate-100 placeholder-slate-400 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 resize-y"
              />
            )}

            {/* File input */}
            {inputMode === 'file' && (
              <div
                onClick={() => !submitting && fileInputRef.current?.click()}
                className={`border-2 border-dashed border-slate-600 rounded-md p-8 text-center cursor-pointer hover:border-slate-500 transition-colors ${submitting ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".log,.txt,.out"
                  onChange={handleFileChange}
                  disabled={submitting}
                  className="hidden"
                />
                <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                {fileName ? (
                  <p className="text-slate-200">{fileName}</p>
                ) : (
                  <p className="text-slate-400">Click to select a log file (.log, .txt, .out)</p>
                )}
                {content && fileName && (
                  <p className="text-slate-500 text-sm mt-1">{content.split('\n').length} lines loaded</p>
                )}
              </div>
            )}
          </div>

          {/* Error */}
          {error && (
            <div className="mb-4 bg-red-900/50 border border-red-700 rounded-md px-4 py-3 text-red-400 text-sm">
              {error}
            </div>
          )}

          {/* Submit button */}
          <button
            type="submit"
            disabled={!canSubmit}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:hover:bg-blue-600 text-white font-semibold py-3 px-4 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-lg"
          >
            {submitting ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Submitting...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5" />
                Submit Log
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}

export default SubmitPage;
