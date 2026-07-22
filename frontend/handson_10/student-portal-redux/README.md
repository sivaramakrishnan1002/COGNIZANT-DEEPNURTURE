# Hands-On 10 - API Layer and Advanced State Management

The app keeps HTTP concerns in `src/api/`, then uses a Redux Toolkit async thunk and selectors. Components receive data/loading/error state rather than Axios responses. React + Redux Toolkit has explicit actions and DevTools; Angular + NgRx adds effects for side effects; Vue + Pinia provides a lighter Composition API store with less boilerplate. `ErrorBoundary` is the application-level fallback UI.
