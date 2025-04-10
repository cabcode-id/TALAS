import CardBeritaCompact from "../components/CardNews/CardBeritaCompact";
import CardBeritaGrid from "../components/CardNews/CardBeritaGrid";
import TopNews from "../components/CardNews/TopNews";
import MainNews from "../components/CardNews/MainNews";
import RecentNews from "../components/CardNews/RecentNews";
import CategoriesCard from "../components/CardNews/CategoriesCard";

function HomePage() {
    return (
      <div className="flex flex-col text-black mx-20">
        <div className="flex flex-row text-black gap-x-20">
            {/* Trending News */}
            <div>
                <MainNews 
                    data={{
                        title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                        description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi non mattis dolor, vel pellentesque augue. Vestibulum sed finibus leo, non sodales odio. Morbi tristique quis orci ac ullamcorper. Proin eget neque vitae metus vehicula mattis sed non nunc. Sed ac ligula vitae arcu convallis tempor sodales in purus. Integer a consequat arcu, quis ultrices nisl. Vivamus in pellentesque lorem. In id egestas turpis. Morbi ornare purus odio, aliquam porttitor urna tristique ac. Praesent mollis leo sem. Proin non nulla sit amet nunc sodales ultrices non ac urna. Proin consectetur sem sed elit ullamcorper porttitor. Aliquam suscipit malesuada dolor, sed venenatis lectus eleifend sed. In laoreet vestibulum neque a eleifend. Donec lacinia placerat diam, in sodales libero euismod ac. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi congue sagittis orci ut sodales. In et vehicula ante. Aliquam a sagittis erat, in bibendum lacus. Quisque ut sapien in leo pretium dictum eget vel nisi. Aenean vel pulvinar turpis. Fusce sagittis urna massa, quis suscipit diam placerat eu. Maecenas mattis justo quis justo condimentum blandit. Maecenas et ante tempus diam consequat consequat. Praesent ut hendrerit eros. Maecenas massa massa, bibendum quis vulputate sit amet, cursus sed ipsum. Nunc eu auctor arcu. Phasellus eleifend rutrum ipsum at congue. Sed auctor leo vitae mi suscipit interdum. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Curabitur vulputate in nisi non posuere. Nullam turpis orci, hendrerit at aliquet vel, elementum at lectus. Aliquam eu erat leo. Aliquam erat volutpat. Ut lectus felis, pretium non libero id, condimentum imperdiet ante. Proin egestas leo nisi, eget consectetur urna hendrerit sit amet. Etiam pharetra finibus posuere. Phasellus nulla tortor, viverra et lectus a, lobortis cursus magna. Nulla at diam id nisl commodo aliquet in non erat.",
                    }}
                />
            </div>

            {/* Top News List */}
            <div>
                <h1 className="font-bold text-2xl">Top News</h1>
                {/* <div className="flex flex-row gap-y-10 mt-5 hover:bg-gray-100 hover:text-white">
                    <p className="mr-5 font-base text-gray-500">01</p>
                    <TopNews 
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                        }}
                    />
                </div> */}
                <div className="flex flex-row gap-y-10 mt-5 hover:bg-gray-100">
                    <p className="mr-5 font-base text-gray-500">01</p>
                    <CategoriesCard
                        data={{
                            name: "Health",
                        }}
                    />
                </div>
                <div className="flex flex-row gap-y-10 mt-5 hover:bg-gray-100">
                    <p className="mr-5 font-base text-gray-500">02</p>
                    <CategoriesCard
                        data={{
                            name: "Politics",
                        }}
                    />
                </div>
                <div className="flex flex-row gap-y-10 mt-5 hover:bg-gray-100">
                    <p className="mr-5 font-base text-gray-500">03</p>
                    <CategoriesCard
                        data={{
                            name: "Sports",
                        }}
                    />
                </div>
                <div className="flex flex-row gap-y-10 mt-5 hover:bg-gray-100">
                    <p className="mr-5 font-base text-gray-500">04</p>
                    <CategoriesCard
                        data={{
                            name: "Technology",
                        }}
                    />
                </div>
            </div>
        </div>

        <hr className="my-7"/>

        {/* Main News */}
        <div>
            <h1 className="text-2xl font-bold">Main</h1>
            <div className="grid grid-cols-2 gap-x-20 gap-y-10 md:grid-cols-2 lg:grid-cols-2 mt-5">
                <CardBeritaCompact
                    data={{
                        title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                    }}
                />
                <CardBeritaCompact
                    data={{
                        title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                    }}
                />
                <CardBeritaCompact
                    data={{
                        title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                    }}
                />
                <CardBeritaCompact
                    data={{
                        title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan"
                    }}
                />
            </div>
        </div>

        <hr className="my-7"/>
        
        {/* Top News Card */}
        <div>
            <h1 className="font-bold text-2xl">Top News</h1>
            <div className="grid gap-x-5 gap-y-10 lg:grid-cols-3 mt-5 ">
                <div>
                <CardBeritaGrid 
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                            description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan" 
                        }}
                    />
                </div>
                <div>
                <CardBeritaGrid 
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                            description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan" 
                        }}
                    />
                </div>
                <div>
                <CardBeritaGrid 
                        data={{
                            title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                            description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan" 
                        }}
                    />
                </div>
            </div>
        </div>
        
        <hr className="my-7"/>

        {/* Recent News */}
        <div className="mb-20">
            <h1 className="font-bold text-2xl">Recent News</h1>
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                }}
            />
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    image: "/icon-news.png"
                }}
            />
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                }}
            />
            <RecentNews 
                data={{
                    title: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    description: "Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan Pemerintah Umumkan Kebijakan Baru untuk Pendidikan",
                    image: "/icon-news.png"
                }}
            />
        </div>
      </div>
    );
  }
  
export default HomePage;  