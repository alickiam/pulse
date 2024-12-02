import YourInteractionsTable from "@/components/interactions-table";
import { Button } from "@/components/ui/button";
import { Poppins } from "next/font/google";
import { withAuth } from "@/lib/auth/protected-route";
import { useUser } from "@/lib/hooks/useUser";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "700"],
});

function Home() {
  const { user, logout } = useUser();

  return (
    <div className={`${poppins.className} min-h-screen p-10 gap-16 bg-gray-900`}>
      <div className="flex justify-between items-center">
        <h3 className="text-2xl font-bold text-left text-white">Hello, {user?.username}</h3>
        <Button variant="outline" onClick={logout}>
          Logout
        </Button>
      </div>
      <YourInteractionsTable />
      <div className="flex justify-center items-center">
        <div className="max-w-4xl w-full mt-16 p-8 rounded-xl bg-gradient-to-br from-purple-100/10 via-pink-100/10 to-red-100/10 backdrop-blur-sm">
          <h2 className="text-4xl font-extrabold text-center bg-gradient-to-r from-purple-400 via-pink-300 to-red-400 text-transparent bg-clip-text animate-gradient mb-8">
            Personalized Feedback
          </h2>

          <div className="space-y-6 text-gray-200">
            {user?.improvement ? (
              <div className="space-y-4">
                <h3 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-blue-400 text-transparent bg-clip-text">
                  Areas for Improvement
                </h3>
                <p className="leading-relaxed whitespace-pre-wrap">{user.improvement}</p>
              </div>
            ) : (
              <div className="space-y-4">
                <h3 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-blue-400 text-transparent bg-clip-text">
                  No Feedback Yet
                </h3>
                <p className="leading-relaxed">
                  Complete more interactions to receive personalized AI feedback on your
                  communication style and relationships.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default withAuth(Home);
