PR_QUERY: str = """
query MyQuery {
  organization(login: \"${organization}\") {
    repository(name: \"${repository}\") {
      id
      name
      url
      pullRequests(first: 100, states: OPEN) {
        nodes {
          author {
            ... on User {
              id
              email
              login
              name
              url
            }
          }
          isDraft
          mergeable
          number
          state
          title
          url
          updatedAt
          createdAt
          labels(first: 10) {
            edges {
              node {
                id
                name
                description
                color
              }
            }
          }
          assignees(first: 100) {
            edges {
              node {
                id
                login
                name
                url
              }
            }
          }
          reviewRequests(first: 10) {
            nodes {
              requestedReviewer {
                ... on User {
                  id
                  email
                  login
                  name
                  url
                }
              }
            }
          }
          reviews(first: 100) {
            nodes {
              state
              url
              author {
                ... on User {
                  id
                  email
                  login
                  name
                  url
                }
              }
              createdAt
              updatedAt
            }
          }
        }
      }
    }
  }
}
"""