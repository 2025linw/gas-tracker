import { useRouter } from 'vue-router';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { doc, getDoc, setDoc } from 'firebase/firestore';
import { useFirebaseAuth, useFirestore } from 'vuefire';


const db = useFirestore();

const googleAuthProvider = new GoogleAuthProvider();

export function useAuth() {
  const auth = useFirebaseAuth()!;
  const router = useRouter();

  const loginWithGoogle = async function () {
    const { user } = await signInWithPopup(auth, googleAuthProvider);

    const ref = doc(db, 'users', user.uid);
    const snap = await getDoc(ref);

    if (!snap.exists()) {
      await setDoc(ref, {
        themePref: 'system',
      });
    }

    router.push('/dashboard');
  };

  return { loginWithGoogle };
}
