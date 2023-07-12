import { describe, test, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { createFetchResponse } from '../utils/test-utils'
import App from '../App'

global.fetch = vi.fn()

beforeEach(() => {
  fetch.mockResolvedValue(createFetchResponse(
    [
      {
        "id": 132983151,
        "invoice_number": "1001",
        "amount": "999.84",
        "due_date": "2023-06-27",
        "borrower_id": 1,
        "created_at": "2023-06-29T14:24:37.029Z",
        "updated_at": "2023-06-29T14:53:37.102Z",
        "state": "closed"
      },
    ]
  ))
})

describe('<App />', () => {
  test('App mounts properly', () => {
    const wrapper = render(<App />)
    expect(wrapper).toBeTruthy()

    const h1 = wrapper.container.querySelector('h1')
    expect(h1?.textContent).toBe('Borrower Invoices')

    const text = screen.getByText(
      /Select a borrower to view their invoices/i
    )

    expect(text.textContent).toBeTruthy()
  })
})
