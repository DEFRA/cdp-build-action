import neostandard from 'neostandard'

export default neostandard({
  env: ['node', 'vitest'],
  ignores: [...neostandard.resolveIgnoresFromGitignore(), './dist/**'],
  noJsx: true,
  noStyle: true
})
