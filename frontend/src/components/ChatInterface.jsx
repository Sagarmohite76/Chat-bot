import React, { useState, useEffect, useRef } from 'react';
import { Send, User, MessageSquare, Plus, Bot, Link, Database } from 'lucide-react';
import IngestForm from './IngestForm';

const ChatInterface = () => {
    const [view, setView] = useState('chat'); // 'chat' or 'knowledge'
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e) => {
        if (e) e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = { text: input, sender: 'user', id: Date.now() };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: userMessage.text,
                    user_id: 1,
                    conversation_id: 1
                }),
            });

            if (!response.ok) throw new Error('Failed to get response');

            const data = await response.json();
            const botMessage = { 
                text: data.message, 
                sender: 'bot', 
                sources: data.sources,
                id: Date.now() + 1 
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Chat Error:', error);
            setMessages(prev => [...prev, { 
                text: "Sorry, I'm having trouble connecting right now.", 
                sender: 'bot', 
                isError: true,
                id: Date.now() + 2 
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const clearChat = () => {
        setMessages([]);
    };

    // Extract unique queries from messages for sidebar history
    const historyItems = messages.filter(m => m.sender === 'user').slice(-10);

    return (
        <div className="app-container">
            <div className="sidebar">
                <div className="brand" style={{ cursor: 'pointer' }} onClick={() => setView('chat')}>
                    <div className="brand-icon">
                        <Bot size={20} color="#000" />
                    </div>
                    TalkingBee
                </div>
                
                <button className="new-chat-btn" onClick={() => { clearChat(); setView('chat'); }}>
                    <Plus size={18} /> New Chat
                </button>

                <div 
                    className={`nav-item ${view === 'knowledge' ? 'active' : ''}`}
                    onClick={() => setView('knowledge')}
                >
                    <Database size={18} /> Knowledge Base
                </div>
                
                <div className="history-list">
                    {historyItems.map((item, index) => (
                        <div key={index} className="history-item">
                            <MessageSquare size={16} />
                            <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                                {item.text}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            <div className="chat-main">
                <div className="chat-header">
                    <div className="status-badge">
                        <div className="status-dot"></div>
                        Online
                    </div>
                </div>

                {view === 'knowledge' ? (
                    <div style={{ flex: 1, display: 'flex', overflowY: 'auto', padding: '2rem' }}>
                        <IngestForm />
                    </div>
                ) : (
                    <>
                        <div className="messages-container">
                            {messages.length === 0 ? (
                                <div className="welcome-screen">
                                    <div className="welcome-icon-wrapper">
                                        <Bot size={40} />
                                    </div>
                                    <h1>Hi, I'm TalkingBee!</h1>
                                    <p>How can I help you today? I'm ready to chat and answer your questions.</p>
                                </div>
                            ) : (
                                messages.map((msg) => (
                                    <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
                                        <div className="avatar">
                                            {msg.sender === 'user' ? <User size={20} /> : <Bot size={20} />}
                                        </div>
                                        <div className="message-content" style={{ width: '100%' }}>
                                            <div className="bubble">
                                                {msg.text}
                                            </div>
                                            {msg.sources && (
                                                <div className="sources-panel">
                                                    <div className="sources-header">
                                                        <Link size={14} /> Sources
                                                    </div>
                                                    <div className="source-items">
                                                        <div className="source-item">
                                                            {msg.sources}
                                                        </div>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                ))
                            )}
                            
                            {isLoading && (
                                <div className="message-wrapper bot">
                                    <div className="avatar">
                                        <Bot size={20} />
                                    </div>
                                    <div className="bubble">
                                        <div className="typing-dots">
                                            <span></span><span></span><span></span>
                                        </div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        <div className="input-area">
                            <div className="input-container">
                                <form className="input-box" onSubmit={handleSend}>
                                    <textarea
                                        value={input}
                                        onChange={(e) => setInput(e.target.value)}
                                        placeholder="Ask TalkingBee anything..."
                                        onKeyDown={(e) => {
                                            if(e.key === 'Enter' && !e.shiftKey) {
                                                e.preventDefault();
                                                handleSend(e);
                                            }
                                        }}
                                        disabled={isLoading}
                                        rows={1}
                                    />
                                    <button type="submit" className="send-btn" disabled={!input.trim() || isLoading}>
                                        <Send size={18} />
                                    </button>
                                </form>
                                <div style={{ textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.75rem' }}>
                                    TalkingBee is here to help you.
                                </div>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default ChatInterface;
