import { useState } from 'react'
import '../App.css'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [welcome, setWelcome] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password })
      })
      const data = await response.json()
      if (data.success) {
        setWelcome(`Welcome, ${data.user.username}!`)
        setMessage('')
      } else {
        setMessage(data.error || 'Login failed')
        setWelcome('')
      }
    } catch (err) {
      setMessage('Network error')
      setWelcome('')
    }
  }

  return (
    <div className="login-wrapper">
      <div className="card">
        <h1>AI Interview Readiness Coach</h1>
        <p className="tagline">Practice smarter. Walk into every interview ready.</p>
        {welcome && <div className="welcome">{welcome}</div>}
        {message && <div className="error">{message}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary">Log In</button>
        </form>
      </div>
    </div>
  )
}

export default Login
