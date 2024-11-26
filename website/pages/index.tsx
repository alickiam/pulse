import YourInteractionsTable from "@/components/interactions-table";
import { Button } from "@/components/ui/button";
import { Poppins } from "next/font/google";

const poppins = Poppins({
  subsets: ["latin"],
  weight: ["400", "700"],
});

export default function Home() {
  return (
    <div className={`${poppins.className} min-h-screen p-10 gap-16 bg-gray-900`}>
      <div className="flex justify-between items-center">
        <h3 className="text-2xl font-bold text-left text-white">Hello, Faisal</h3>
        <Button variant="outline">Logout</Button>
      </div>
      <YourInteractionsTable />
      <div className="flex justify-center items-center">
        <div className="max-w-4xl w-full mt-16 p-8 rounded-xl bg-gradient-to-br from-purple-100/10 via-pink-100/10 to-red-100/10 backdrop-blur-sm">
          <h2 className="text-4xl font-extrabold text-center bg-gradient-to-r from-purple-400 via-pink-300 to-red-400 text-transparent bg-clip-text animate-gradient mb-8">
            AI Feedback
          </h2>
          
          <div className="space-y-6 text-gray-200">
            <div className="space-y-4">
              <h3 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-blue-400 text-transparent bg-clip-text">
                Interaction Analysis
              </h3>
              <p className="leading-relaxed">
                Based on your recent interactions, you show strong engagement with people who share your intellectual interests and hobbies. Your conversations with Emma and Liam demonstrate your ability to maintain meaningful discussions on diverse topics. However, you could benefit from initiating more activities outside of conversations, like the salsa classes discussed with Sophia.
              </p>
            </div>

            <div className="space-y-4">
              <h3 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-blue-400 text-transparent bg-clip-text">
                Action Items
              </h3>
              <ul className="list-disc list-inside space-y-2">
                <li>Schedule the salsa class with Sophia to transform conversations into shared experiences</li>
                <li>Follow up with Emma about environmental causes - consider joining or organizing an activity together</li>
                <li>Engage more on social platforms where your matches are active (Instagram, Discord)</li>
                <li>Plan a cooking session with Liam to combine your shared interests</li>
              </ul>
            </div>

            <div className="space-y-4">
              <h3 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-blue-400 text-transparent bg-clip-text">
                Areas for Growth
              </h3>
              <ul className="list-disc list-inside space-y-2">
                <li>Diversify your conversation topics beyond shared interests</li>
                <li>Take more initiative in planning real-world meetups</li>
                <li>Maintain consistent communication across different platforms</li>
                <li>Balance deep discussions with lighter, casual conversations</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
