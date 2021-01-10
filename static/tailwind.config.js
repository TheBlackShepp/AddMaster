// tailwind.config.js
module.exports = {
    purge: [],
    darkMode: 'media', // or 'media' or 'class'
    theme: {
      extend: {
          colors: {
            brown: {
                300: '#C38E70',
                400: '#9D6B53',
                600: '#8A5A44',
                700: '#774936'
            }
          },
          borderWidth:{
            '1': '1px'
          }

      },
    },
    variants: {},
    plugins: [],
  }