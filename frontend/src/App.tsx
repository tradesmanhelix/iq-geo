import { useState } from 'react'
import { useEffect } from 'react'
import { useCallback } from "react"

import { Invoice } from "./components/Invoice.tsx"

function getBorrowers() {
  return fetch('/api/v1/borrowers')
    .then(data => data.json())
}

function App() {
  const [borrowers, setBorrowers] = useState<Object[]>([])
  const [borrowerId, setBorrowerId] = useState<number>(0)

  const [invoices, setInvoices] = useState<Object[]>([])

  useEffect(() => {
    let mounted = true
    getBorrowers()
      .then(borrowers => {
        if(mounted) {
          setBorrowers(borrowers)
        }
      })
    return () => mounted = false
  }, [])

  const fetchInvoices = useCallback((newBorrowerId: number) => {
    if (newBorrowerId == borrowerId) return

    setBorrowerId(newBorrowerId)

    fetch(`/api/v1/borrowers/${newBorrowerId}/invoices`)
      .then(data => data.json())
        .then(invoices => {
          setInvoices(invoices)
        })
  }, [borrowerId])

  return (
    <main className="my-4">
      <div className="container">
        <div className="row">
          <div className="col">
            <h1>Borrower Invoices</h1>
            <p className="lead">Select a borrower to view their invoices</p>
            <hr />
          </div>
        </div>
        <div className="row">
          <div className="col-lg-4">
            <div>
              <ul style={{ cursor: "pointer", marginBottom: "0.5rem", textAlign: "left" }}>
                {
                  borrowers.map(mapped => (
                    <li
                      style={{ marginBottom: "1.5rem" }}
                      key={mapped.id}
                      onClick={() => fetchInvoices(mapped.id)}
                    >{mapped.name}</li>
                  ))
                }
              </ul>
            </div>
          </div>
          <div className="col">
            <div className="row g-4">
              { invoices.length ?
                invoices.map(mapped => (
                  <Invoice
                    key={mapped.id}
                    invoiceId={mapped.id}
                    invoiceNumber={mapped.invoice_number}
                    amount={mapped.amount}
                    dueDate={mapped.due_date}
                    invoiceState={mapped.state}
                  />
                )) : <p>No invoices</p>
              }
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}

export default App
