module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      "process.env.PERSON_SVC_HOST": JSON.stringify(
        process.env.PERSON_SVC_HOST
      ),
      "process.env.CONN_SVC_HOST": JSON.stringify(process.env.CONN_SVC_HOST),
    }),
  ],
};
