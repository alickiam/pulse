"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useUser } from "@/lib/hooks/useUser";
import { useRouter } from "next/router";
import { toast } from "sonner";

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useUser();
  const router = useRouter();

  async function onSubmit(event: React.SyntheticEvent) {
    event.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Failed to login');
      }

      if (data.success && data.user) {
        login(data.user);
        toast.success('Login successful');
        router.push('/');
      }
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Failed to login');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col justify-center items-center p-4">
      <div className="w-full max-w-md">
        <h1 className="text-4xl font-extrabold text-center bg-gradient-to-r from-purple-400 via-pink-300 to-red-400 text-transparent bg-clip-text animate-gradient mb-8">
          Login to Your Account
        </h1>
        <div className="bg-gradient-to-br from-purple-100 via-pink-100 to-red-100 p-1 rounded-xl glow-border">
          <form onSubmit={onSubmit} className="bg-gray-900 rounded-lg p-6 space-y-6">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-white">
                Username
              </Label>
              <Input
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                type="text"
                autoCapitalize="none"
                autoComplete="username"
                autoCorrect="off"
                disabled={isLoading}
                className="bg-gray-800 border-purple-500 text-white placeholder-gray-400"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password" className="text-white">
                Password
              </Label>
              <Input
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                type="password"
                autoCapitalize="none"
                autoComplete="current-password"
                disabled={isLoading}
                className="bg-gray-800 border-purple-500 text-white placeholder-gray-400"
                required
              />
            </div>
            <Button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold py-2 px-4 rounded-full transition-all duration-300 transform hover:scale-105"
            >
              {isLoading && <span className="mr-2 h-4 w-4 animate-spin">⌛</span>}
              Sign In
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
