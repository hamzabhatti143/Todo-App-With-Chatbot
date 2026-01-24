/**
 * Custom Events System
 *
 * Simple event emitter for cross-component communication.
 */

type EventCallback = () => void

class EventEmitter {
  private events: Map<string, EventCallback[]> = new Map()

  on(event: string, callback: EventCallback): void {
    if (!this.events.has(event)) {
      this.events.set(event, [])
    }
    this.events.get(event)!.push(callback)
  }

  off(event: string, callback: EventCallback): void {
    const callbacks = this.events.get(event)
    if (callbacks) {
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  emit(event: string): void {
    const callbacks = this.events.get(event)
    if (callbacks) {
      callbacks.forEach((callback) => callback())
    }
  }
}

export const appEvents = new EventEmitter()

// Event types
export const APP_EVENTS = {
  USER_LOGGED_IN: 'user:logged_in',
  USER_LOGGED_OUT: 'user:logged_out',
} as const
