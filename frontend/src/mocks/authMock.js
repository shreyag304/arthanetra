export async function login(mobile) {

  return new Promise((resolve, reject) => {

    setTimeout(() => {

      if (!mobile || mobile.length < 10) {

        reject(new Error("Invalid mobile number"));

        return;

      }

      resolve({

        token: "mock-token",

        user: {

          id: "1",

          name: "Shreya",

          mobile,

          language: "English"

        }

      });

    }, 600);

  });

}