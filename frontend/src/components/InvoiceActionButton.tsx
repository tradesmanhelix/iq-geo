import { useCallback } from 'react'
import { useEffect } from 'react'
import { useState } from 'react'
import { useReducer } from 'react'

type InvoiceActionButtonProps = {
  invoiceId: number
  invoiceNumber: string
  invoiceState: string
  setInvoiceStatus: (newStatus: string) => void
}

function getCreatedStateButtons(invoiceId: number, invoiceNumber: string, updateInvoiceState: Function) {
  const approveArgs = { invAction: "approve", invNum: invoiceNumber, invId: invoiceId }
  const rejectArgs = { invAction: "reject", invNum: invoiceNumber, invId: invoiceId }

  return (
    <div className="d-grid gap-2">
      <button
        className="btn btn-primary"
        onClick={() => confirmAction(approveArgs) && updateInvoiceState("approved", invoiceId)}
      >Approve</button>
      <button
        className="btn btn-outline-danger"
        onClick={() => confirmAction(rejectArgs) && updateInvoiceState("rejected", invoiceId)}
      >Reject</button>
    </div>
  )
}

function getApprovedStateButtons(invoiceId: number, invoiceNumber: string, updateInvoiceState: Function) {
  const purchaseArgs = { invAction: "purchase", invNum: invoiceNumber, invId: invoiceId }

  return (
    <div className="d-grid gap-2">
      <button
        className="btn btn-success"
        onClick={() => confirmAction(purchaseArgs) && updateInvoiceState("purchased", invoiceId)}
      >Purchase</button>
    </div>
  )
}

function getPurchasedStateButtons(invoiceId: number, invoiceNumber: string, updateInvoiceState: Function) {
  const closeArgs = { invAction: "close", invNum: invoiceNumber, invId: invoiceId }

  return (
    <div className="d-grid gap-2">
      <button
        className="btn btn-secondary"
        onClick={() => confirmAction(closeArgs) && updateInvoiceState("closed", invoiceId)}
      >Close</button>
    </div>
  )
}

function confirmAction(action) {
  return confirm(`Are you sure you want to ${action.invAction} the invoice #${action.invNum}?`)
}

export function InvoiceActionButton({ invoiceId, invoiceNumber, invoiceState, setInvoiceStatus }: InvoiceProps) {

  const updateInvoiceState = useCallback((newState: string, invoiceId: string) => {
    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ invoice: { state: newState }})
    };

    fetch(`/api/v1/invoices/${invoiceId}`, requestOptions)
      .then(response => response.json())
      .then(data => {
        setInvoiceStatus(data.state)
      })
  }, [])

  const buttonsForInvoiceState = useCallback((invoiceState: string) => {
    switch (invoiceState) {
      case "created":
        return getCreatedStateButtons(invoiceId, invoiceNumber, updateInvoiceState)
        break
      case "approved":
        return getApprovedStateButtons(invoiceId, invoiceNumber, updateInvoiceState)
        break
      case "purchased":
        return getPurchasedStateButtons(invoiceId, invoiceNumber, updateInvoiceState)
        break
      case "rejected":
      case "closed":
        break
      default:
        console.error(`Invalid state: ${invoiceState}`)
    }
  }, [])

  return (
    <>
      {buttonsForInvoiceState(invoiceState)}
    </>
  )
}
